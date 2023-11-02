#!/usr/bin/env python3
"""
Created on Mon Jun 7 23:47:19 2021

MultiVuServer.py is a module for use on a computer running MultiVu.  It can
be used with MultiVuClient.py to control a Quantum Design cryostat.

@author: D. Jackson
"""

import sys
import socket
import selectors
import threading
import time
from typing import Union, Dict, List


from .SocketMessageServer import ServerMessage
from .ParseInputs import Inputs
from .QdCommandParser import QdCommandParser
from .instrument import Instrument
from .exceptions import MultiPyVuException
from .create_logger import log
from .project_vars import (TIMEOUT_LENGTH,
                           SERVER_NAME,
                           )

if sys.platform == 'win32':
    try:
        import msvcrt    # Used to help detect the esc-key
    except ImportError:
        print("Must import the pywin32 module.  Use:  ")
        print("\tconda install -c conda-forge pywin32")
        print("   or")
        print("\tpip install pywin32")
        sys.exit(0)


class Server():
    def __init__(self,
                 flags: List[str] = [],
                 keep_server_open=False
                 ):
        '''
        This class is used to start and maintain a socket server.  A client
        can be set up using MultiVuClient.py.

        Parameters
        ----------
        flags : [str], optional
            For a list of flags, use the help flag, '--help'.  The default
            is []. 
            Arguments are:
            --h(elp) to display the help text
            --s for scaffolding in order to simulate the script
            --ip=<host address> to specify the host IP
                address (default = 'localhost')
            --p(ort) to specify the port (default is 5000)
            --v(erbose) to turn on the verbose text when the server
                sends/receives info

            An argument without a flag is the instrument.
            The default IP address is 'localhost,' and the default port
            is 5000.
        keep_server_open : bool, optional
            This flag can be set to true when running the server in its own
            script.  When True, the script will stay in the .open() method
            as long as the server is running.
            Default is False.

        '''

        # The normal behavior of MultiVuServer runs the server in a separate
        # thread. In order to keep the server open when running the server
        # alone, one does not want to use threading.
        run_with_threading = not keep_server_open

        self.lsock = None
        self.message = None     # ServerMessage object
        self._client_connected = False
        # Set the flags used with threading
        self._thread_running = False
        # this is a threading.Event() object
        self._stop_event = None
        # Parsing the flags looks for user
        try:
            flag_info = self._parse_input_flags(flags)
        except UserWarning as e:
            # This happens if it is displaying the help text
            self.log_event = log()
            self.logger = self.log_event.create(SERVER_NAME, False)
            self.logger.info(e)
            sys.exit(0)
        self.verbose = bool(flag_info['verbose'])
        self.scaffolding = bool(flag_info['scaffolding_mode'])
        # Update the host member variable if the user flags selected one
        self.host = flag_info['host']
        self.port = flag_info['port']
        self._addr = (self.host, self.port)

        # Configure logging
        self.log_event = log(SERVER_NAME)
        self.logger = self.log_event.create(SERVER_NAME,
                                            run_with_threading,
                                            )

        # Instantiate the Instrument class
        try:
            self.instr = Instrument(flag_info['instrument_str'],
                                    self.scaffolding,
                                    run_with_threading,
                                    self.verbose)
        except MultiPyVuException:
            good_exit = self.close()
            if not good_exit:
                sys.exit(0)
        # Create a threading event
        if run_with_threading:
            self._stop_event = threading.Event()

    def config_sock(self) -> None:
        # Set up the sockets
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Avoid bind() exception: OSError: [Errno 48] Address already in use
        self.lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.lsock.bind(self._addr)
        except OSError as e:
            # connection already open?
            self.logger.info(e)
            return
        self.lsock.listen()
        self.lsock.setblocking(False)
        self.logger.info(f'Listening on {self._addr}')

    def __enter__(self):
        self.config_sock()
        quit_keys = "ctrl-c"
        if sys.platform == 'win32':
            quit_keys = "ESC"
        self.logger.info(f'Press {quit_keys} to exit.')

        # The selectors must be first configured here, before
        # starting the _monitor_socket_connection thread.  This
        # was the only way I could get pywin32com to work with
        # threading
        sel = selectors.DefaultSelector()
        sel.register(self.lsock, selectors.EVENT_READ, data=None)

        # Call ._monitor_socket_connection()
        if self._stop_event is not None:
            self.server_thread = threading.Thread(
                name=SERVER_NAME,
                target=self._monitor_socket_connection,
                args=[sel]
                )
            # The Server thread is now doing most of the work
            self._thread_active = True
            self.server_thread.start()
        else:
            try:
                self._monitor_socket_connection(sel)
            except KeyboardInterrupt:
                if self.message is not None:
                    self.message.shutdown()
                    self.message = None
                self.close()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> bool:
        if self.message is not None:
            self.instr.end_multivu_win32com_instance()
            self.message.shutdown()
        if self.lsock is not None:
            if self.lsock.fileno() > 0:
                try:
                    self.lsock.close()
                except OSError as e:
                    msg = 'error: socket.close() exception for '
                    msg += f'{self._addr}: {repr(e)}'
                    self.logger.info(msg)
                finally:
                    # Delete reference to socket object for garbage collection
                    self.lsock = None
        self._thread_active = False
        if self._stop_event is not None:
            self._stop_event.set()

        # Error handling
        safe_exit = True
        if isinstance(exc_value, KeyboardInterrupt):
            self._update_connection_status(True)
            self.logger.info('')
            self.logger.info('Caught keyboard interrupt, exiting')
            safe_exit = True
        elif isinstance(exc_value, MultiPyVuException):
            self.logger.info(exc_value)
            safe_exit = False
        elif isinstance(exc_value, UserWarning):
            # Display the help and quit.
            self.logger.info(exc_value)
            safe_exit = True
        elif isinstance(exc_value, ConnectionError):
            safe_exit = True
        elif isinstance(exc_value, Exception):
            msg = 'MultiVuServer: error: exception for '
            if self.message is not None:
                msg += f'{self.message.addr}'
            msg += f':  {exc_value}'
            self.logger.info(msg)
            safe_exit = False
        else:
            safe_exit = True
        self.log_event.remove()
        return safe_exit

    def _update_connection_status(self, connected):
        with threading.Lock():
            self._client_connected = connected
            self._addr = None if not connected else self._addr
        if not connected:
            self.close()

    @property
    def _thread_active(self):
        with threading.Lock():
            return self._thread_running

    @_thread_active.setter
    def _thread_active(self, active):
        with threading.Lock():
            if self._thread_running and not active:
                self._stop_event.set()
            self._thread_running = active

    def _parse_input_flags(self,
                           flags: List[str]
                           ) -> Dict[str, Union[str, bool, None]]:
        '''
        This routine will determine what the list of flags mean. If either
        the flag (--t) or the threading input-parameter are true, the server
        will be run in its own thread

        Parameters
        ----------
        flags : [str]
            Input flags such as -h or -s and PPMS flavor.  Note that any
            options specified by the command line arguments (these flags)
            will overwrite any parameters passed when instantiating the class.

        Returns
        -------
        dict()
            Dictionary with keys: 'instrument_str',
                                  'run_with_threading',
                                  'scaffolding_mode',
                                  'host',
                                  'verbose'.

        '''
        user_input = Inputs()
        return_flags = user_input.parse_input(flags)

        return return_flags

    def _accept_wrapper(self, sel: selectors.DefaultSelector,
                        sock: Union[socket.socket, None] = None
                        ) -> ServerMessage:
        '''
        This method accepts a new client.

        Parameters:
        -----------
        sel : selectors.DefaultSelector
            This manages the socket connections.
        sock : socket.socket (optional)
            This contains the socket information.
            Default: None - uses self.lsock
        '''
        # Connect to MultiVu in order to enable a new thread
        self.instr.get_multivu_win32com_instance()

        # get the sock to be ready to read
        if sock is None:
            sock = self.lsock
        if sock is None:
            msg = 'Must supply a socket.socket (self.lsock is None)'
            raise ValueError(msg)
        accepted_sock, self._addr = sock.accept()
        accepted_sock.setblocking(False)
        self.logger.info(f'Accepted connection from {self._addr}')

        self.qd_command = QdCommandParser(self.instr)
        message = ServerMessage(sel,
                                accepted_sock,
                                self.qd_command,
                                self.verbose,
                                self.scaffolding,
                                self._stop_event is not None,
                                )

        message.register_read_socket()
        self._update_connection_status(True)
        return message

    def _check_windows_esc(self) -> None:
        '''
        Windows looks for the ESC key to quit.

        Raises:
        -------
        Throws a KeyboardInterrupt if the esc key is hit.
        '''
        if sys.platform == 'win32':
            if (msvcrt.kbhit()
                    and msvcrt.getch().decode() == chr(27)):
                raise KeyboardInterrupt

    def _monitor_socket_connection(self, selectors: selectors.DefaultSelector):
        '''
        This monitors traffic and looks for new clients and new requests.  For
        new clients, it calls ._accept_wrapper.  After that, it takes the
        socket and asks the SocketMessageServer for help in figuring out what
        to do.

        Parameters:
        -----------
        sel : selectors.DefaultSelector
            This manages the socket connections.

        Raises:
        -------
        KeyboardInterrupt
            Keyboard interrupts are how the user closes the server.

        Returns:
        --------
        None.

        '''
        if self._stop_event is not None:
            self._stop_event.wait(1)
        if self.lsock is None:
            self._update_connection_status(False)
            return

        while True:
            if self._stop_event is not None:
                if self._stop_event.is_set():
                    return
            self._check_windows_esc()
            try:
                events = selectors.select(timeout=TIMEOUT_LENGTH)
            except OSError:
                # This error happens if the selectors is unavailable.
                continue
            for key, mask in events:
                message = key.data
                selector_sock = key.fileobj
                if message is None:
                    try:
                        message = self._accept_wrapper(selectors, selector_sock)
                    except BlockingIOError:
                        # try calling this method again
                        time.sleep(0.5)
                        continue
                    else:
                        self.message = message
                        # pause to allow for the connection
                        time.sleep(0.5)
                try:
                    message.process_events(mask)
                except ConnectionAbortedError:
                    content = message.request['content']
                    query = content.get('query', 'CLOSE')
                    if query == 'CLOSE':
                        [new_events] = message.get_events(TIMEOUT_LENGTH)
                        new_sock = new_events[0].fileobj
                        self._accept_wrapper(selectors, new_sock)
                        continue
                    else:
                        self._update_connection_status(False)
                    return
                except ConnectionError as e:
                    self.logger.info(e)
                    self._update_connection_status(False)
                    return
                except AttributeError as e:
                    msg = 'Lost connection to socket.'
                    self.logger.info(f'{msg}:   {e}')
                    self._update_connection_status(False)
                    return
                except BaseException as e:
                    self.logger.info(e)
                    return
                else:
                    self._check_windows_esc()
            if self.instr.run_with_threading:
                if not self._thread_active:
                    return

    def open(self):
        '''
        This method is the entry point to the MultiVuServer class.  It starts
        the connection and passes off control to the rest of the class to
        monitor traffic in order to  receive commands from a client and
        respond appropriately.

        Returns
        -------
        None.

        '''
        self.__enter__()

    def close(self) -> bool:
        '''
        This closes the server

        Returns
        -------
        Bool, with True meaning no unknown errors.  False
        signals an unexpected error.
        '''
        err_info = sys.exc_info()
        return self.__exit__(err_info[0],
                             err_info[1],
                             err_info[2])

    def is_client_connected(self) -> bool:
        with threading.Lock():
            status = False
            if self.message is not None:
                status = self.message.connected
            return status

    def client_address(self):
        with threading.Lock():
            if self.is_client_connected():
                address = self.message.addr
            else:
                address = ('', 0)
            return address


def server(flags: str = ''):
    '''
    This method is called when MultiVuServer.py is run from a command line.
    It deciphers the command line text, and the instantiates the
    MultiVuServer.

    Parameters
    ----------
    flags : str, optional
        The default is ''.

    Returns
    -------
    None.

    '''

    user_flags = []
    if flags == '':
        user_flags = sys.argv[1:]
    else:
        user_flags = flags.split(' ')

    s = Server(user_flags, keep_server_open=True)
    s.open()


if __name__ == '__main__':
    server()

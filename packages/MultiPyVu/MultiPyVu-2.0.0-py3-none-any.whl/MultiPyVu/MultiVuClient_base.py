#!/usr/bin/env python3
"""
Created on Mon Jun 7 23:47:19 2021

MultiVuClient_base.py is a module for use on a network that has access to a
computer running MultiVuServer.py.  By running this client, a python script
can be used to control a Quantum Design cryostat.

This is the base class.  It has the basic communication commands.  The
MultiVuClient class has specific commands to be used with this class.

@author: D. Jackson
"""

import sys
import socket
import traceback
import time
from typing import Dict


from .SocketMessageClient import ClientMessage
from .create_logger import log
from .project_vars import (TIMEOUT_LENGTH,
                           CLIENT_NAME,
                           HOST,
                           PORT,
                           )
from .exceptions import MultiPyVuException

if sys.platform == 'win32':
    try:
        import msvcrt    # Used to help detect the esc-key
    except ImportError:
        print("Must import the pywin32 module.  Use:  ")
        print("\tconda install -c conda-forge pywin32")
        print("   or")
        print("\tpip install pywin32")
        sys.exit(0)


MAX_TRIES = 3


class ClientBase():
    '''
    This class is used for a client to connect to a computer with
    MutliVu running MultiVuServer.py.

    Parameters
    ----------
    host: str (optional)
        The IP address for the server.  Default is 'localhost.'
    port: int (optional)
        The port number to use to connect to the server.
    '''

    def __init__(self, host: str = HOST, port: int = PORT):
        self._addr = (host, port)
        self._message = None     # ClientMessage object
        self.sock = None
        self._request = {}
        self._response = {}
        self._thread_running = False
        self.log_event = log(CLIENT_NAME)
        self.instr = None
        self.instrument_name = ''

    def __enter__(self):
        # Configure logging
        self.logger = self.log_event.create(CLIENT_NAME,
                                            display_logger_name=True,
                                            )
        self.logger.info(f'Starting connection to {self._addr}')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.sock.connect_ex(self._addr)

        self._message = ClientMessage(self.sock)
        # send a request to the sever to confirm a connection
        action = 'START'
        for attempt in range(MAX_TRIES):
            try:
                response = self._send_and_receive(action)
            except OSError as e:
                # this includes ConnectionError
                msg = f'Attempt {attempt + 1} of {MAX_TRIES} failed:  {e}'
                self.logger.info(msg)
                if attempt == MAX_TRIES - 1:
                    err_msg = 'Failed to make a connection to the '
                    err_msg += 'server.  Check if the MultiVuServer '
                    err_msg += 'is running.'
                    self.logger.info(err_msg)
                    self._close_and_exit()
                    sys.exit(0)
                time.sleep(1)
            except MultiPyVuException as e:
                self.logger.info(e)
                self._close_and_exit()
                sys.exit(0)
            else:
                self.logger.info(response['result'])
                self.instr = self._message.instr
                self.instrument_name = self._message.instr.name
                break
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        exit_without_error = False
        # Error handling
        if isinstance(exc_value, SystemExit):
            exit_without_error = True
        if isinstance(exc_value, KeyboardInterrupt):
            self.logger.info('')
            self.logger.info('Caught keyboard interrupt, exiting')
            exit_without_error = True
        elif isinstance(exc_value, ConnectionAbortedError):
            msg = 'Shutting down the server.'
            self.logger.info(msg)
            exit_without_error = True
        elif isinstance(exc_value, ConnectionError):
            # Note that ConnectionAbortedError and ConnectionRefusedError
            # are subclasses of ConnectionError
            exit_without_error = True
        elif isinstance(exc_value, MultiPyVuException):
            # Connection closed by the server
            self.logger.info(traceback.format_exc())
            exit_without_error = False
        elif isinstance(exc_value, BaseException):
            msg = 'MultiVuClient: error: exception for '
            if self._message is not None:
                msg += f'{self._message.addr}:'
            msg += f'\n{traceback.format_exc()}'
            self.logger.info(msg)
            exit_without_error = False
        else:
            try:
                self._send_and_receive('CLOSE')
            except ConnectionError:
                exit_without_error = True
            except TimeoutError:
                exit_without_error = True

        # Close things up for all cases
        self._thread_running = False
        if self._message is not None:
            self._message.shutdown()
            self._message = None
        if self.sock is not None:
            self.sock.close()
        time.sleep(1)
        if not exit_without_error:
            self.logger.info(traceback.format_exc())
        self.log_event.remove()
        self.log_event.shutdown()
        self.instr = None
        self.instrument_name = ''
        return exit_without_error

    ###########################
    #  Client Methods
    ###########################

    def open(self):
        '''
        This is the entry point into the MultiVuClient.  It connects to
        a running MultiVuServer

        Parameters
        ----------
        host : str
            The host IP address.  If the server is running on the same
            computer, it is should be 'localhost.'  The host must match
            the IP address of the server.
        port : int
            The port must match the port number for the Server, which is 5000.

        Raises
        ------
        ConnectionRefusedError
            This is raised if there is a problem connecting to the server. The
            most common issue is that the server is not running.

        Returns
        -------
        None.

        '''
        self.__enter__()

    def close_client(self):
        '''
        This command closes the client, but keeps the server running
        '''
        self._close_and_exit()

    def close_server(self):
        '''
        This command closes the server
        '''
        try:
            self._send_and_receive('EXIT')
        except ConnectionAbortedError:
            self._close_and_exit()
        except ConnectionError:
            # print('Error:')
            # # err_info = sys.exc_info()
            # # traceback.print_tb(err_info[2], limit=1)
            # msg = 'No connection to the server.  Is the client connected?'
            # print(msg)
            self._close_and_exit()

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

    def _send_and_receive(self,
                          action: str,
                          query: str = '') -> Dict[str, str]:
        '''
        This takes an action and a query, and sends it to
        ._monitor_and_get_response() to let that method figure out what
        to do with the information.

        Parameters
        ----------
        action : str
            The general command going to MultiVu:  TEMP(?), FIELD(?), and
            CHAMBER(?).  If one wants to know the value of the action, then
            it ends with a question mark.  If one wants to set the action in
            order for it to do something, then it does not end with a question
            mark.
        query : str, optional
            The query gives the specifics of the command going to MultiVu.  For
            queries. The default is '', which is what is used when the action
            parameter ends with a question mark.

        Returns
        -------
        The response dictionary from the ClientMessage class.

        Raises:
        -------
        ConnectionError
        KeyboardInterrupt
        MultiVuException
        '''
        if self._message is None:
            msg = 'Error:  '
            msg += 'No connection to the server.  Is the client connected?'
            raise ConnectionError(msg)
        timeout_attempts = 0
        while True:
            self._message.create_request(action, query)
            try:
                response = self._monitor_and_get_response()
                break
            except TimeoutError:
                timeout_attempts += 1
                if timeout_attempts > MAX_TRIES:
                    # An empty list means the selector timed out
                    msg = 'Socket timed out after '
                    msg += f'{timeout_attempts} attempts.'
                    raise TimeoutError(msg)
        if response == {}:
            msg = 'MultiVuError:  No return value, which could mean that '
            msg += 'MultiVu is not running or that the connection has '
            msg += 'been closed.'
            self.logger.info(msg)
            raise MultiPyVuException(msg)
        # reset the request and response to blank dicts
        self._request = {}
        self._response = {}
        return response

    def query_server(self, action: str,
                     query: str = '') -> Dict[str, str]:
        '''
        Queries the server using the action and query parameters.

        Parameters
        ----------
        action : str
            The general command going to MultiVu:  TEMP(?), FIELD(?), and
            CHAMBER(?), etc..  If one wants to know the value of the action,
            then it ends with a question mark.  If one wants to set the action
            in order for it to do something, then it does not end with a
            question mark.
        query : str, optional
            The query gives the specifics of the command going to MultiVu.  For
            queries. The default is '', which is what is used when the action
            parameter ends with a question mark.

        Returns
        -------
        The response dictionary from the ClientMessage class.

        '''
        try:
            resp: dict = self._send_and_receive(action, query)
        except ConnectionError as e:
            resp = {'action': action,
                    'query': query,
                    'result': str(e)}
            self._close_and_exit()
        return resp

    def _monitor_and_get_response(self) -> Dict[str, str]:
        '''
        This monitors the traffic going on.  It asks the SocketMessageClient
        class for help in understanding the data.  This is also used to handle
        the possible errors that SocketMessageClient could generate.

        Raises
        ------
        ConnectionRefusedError
            Could be raised if the server is not running.
        ConnectionError
            Could be raised if there are connection issues with the server.
        KeyboardInterrupt
            This is used by the user to close the connection.
        MultiVuExeException
            Raised if there are issues with the request for MultiVu commands.

        Returns
        -------
        TYPE
            The information retrieved from the socket and interpreted by
            SocketMessageClient class.

        '''
        # increase the timeout length to make it easier to debug the code
        # and give extra time to make the connection.  If the timeout is
        # set to None it will block until a connection is made.
        timeout = TIMEOUT_LENGTH * 2.5
        # timeout = None
        # TODO - add a counter here and if a connection fails after
        # so many attempts, bring up a question for the user if they
        # want to continue (which would reset the counter) or quit.
        while True:
            events = self._message.get_events(timeout)
            if events:
                # mask = 1 is read
                # mask = 2 is write
                for key, mask in events:
                    message = key.data
                    try:
                        message.process_events(mask)
                    except ConnectionAbortedError as e:
                        # Client closed the server
                        if self._request['action'] == 'EXIT':
                            self._message.close()
                        raise ConnectionAbortedError from e
                    except ConnectionError as e:
                        # Client closed the client
                        raise ConnectionError from e
                    except MultiPyVuException as e:
                        # General MultiPyVu error
                        raise MultiPyVuException(e)
                    except Exception:
                        self._close_and_exit()
                    else:
                        self._check_windows_esc()
                        if message.is_write(mask):
                            self._request = message.request['content']
                        elif message.is_read(mask):
                            self._response = message.response
                            # check response answers a request
                            if self._request['action'] != self._response['action']:
                                msg = 'Received a response to the '
                                msg += 'wrong request:\n'
                                msg += f' request = {self._request}\n'
                                msg += f'response = {self._response}'
                                self.logger.info(msg)
                                raise MultiPyVuException(msg)
                            # return the response
                            rslt = self._response['result']
                            if rslt.startswith('MultiVuError:'):
                                self.logger.info(self._response['result'])
                                message.close()
                                raise MultiPyVuException(rslt)
                            else:
                                return self._response
                        else:
                            raise IndexError
            else:
                # timeout_attempts += 1
                # if timeout_attempts > MAX_TRIES:
                #     # An empty list means the selector timed out
                #     msg = 'Socket timed out after '
                #     msg += f'{timeout} seconds.'
                #     raise TimeoutError(msg)
                # self._message.create_request('START', '')
                raise TimeoutError
            # Check for a socket being monitored to continue.
            if self._message is None \
                    or not self._message.connection_good():
                msg = 'MultiVuError:  Connection disrupted in '
                msg += 'MultiVuClient.py Socket connection broken '
                msg += 'in _monitor_and_get_response()'
                self.logger.info(msg)
                raise MultiPyVuException(msg)

    def _close_and_exit(self):
        err_info = sys.exc_info()
        self.__exit__(err_info[0], err_info[1], err_info[2])

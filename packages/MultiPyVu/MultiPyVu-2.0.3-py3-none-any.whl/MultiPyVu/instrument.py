"""
instrument.py is used to hold information about MultiVu.  It has
the various flavors, and can determine which version of MultiVu is installed
on a machine.

Created on Tue May 18 13:14:28 2021

@author: djackson
"""

import sys
import subprocess
import time
import re
import logging
from enum import Enum, auto

from .project_vars import SERVER_NAME
from .exceptions import MultiPyVuException
from .__version import __version__ as mpv_version

if sys.platform == 'win32':
    try:
        import pythoncom
        import win32com.client as win32
    except ImportError:
        print("Must import the pywin32 module.  Use:  ")
        print("\tconda install -c conda-forge pywin32")
        print("   or")
        print("\tpip install pywin32")
        sys.exit(0)


class InstrumentList(Enum):
    DYNACOOL = auto()
    PPMS = auto()
    VERSALAB = auto()
    MPMS3 = auto()
    OPTICOOL = auto()
    na = auto()


class Instrument():
    def __init__(self,
                 flavor: str = '',
                 scaffolding_mode: bool = False,
                 run_with_threading: bool = False,
                 verbose: bool = False
                 ):
        '''
        This class is used to detect which flavor of MultiVu is installed
        on the computer.  It is also used to return the name of the .exe
        and the class ID, which can be used by win32com.client.

        Parameters
        ----------
        flavor : string, optional
            This is the common name of the MultiVu flavor being used.  If
            it is left blank, then the class finds the installed version
            of MultiVu to know which flavor to use.  The default is ''.
        scaffolding_mode : bool, optional
            This flag puts the class in scaffolding mode, which simulates
            MultiVu.  The default is False.
        run_with_threading : bool, optional
            This flag is used to configure win32com.client to be used in
            a separate thread.  The default is False.
        verbose : bool, optional
            When set to True, the flavor of MultiVu is displayed
            on the command line. The default is False.
        '''
        self.logger = logging.getLogger(SERVER_NAME)
        self.scaffolding_mode = scaffolding_mode
        self.run_with_threading = run_with_threading
        self.verbose = verbose

        self.name = ''
        if flavor == '':
            if self.scaffolding_mode:
                err_msg = 'Must choose a MultiVu flavor to run in '
                err_msg += 'scaffolding mode.'
                for f in InstrumentList:
                    err_msg += f'\n\t{f.name}' if f != f.na else ''
                raise MultiPyVuException(err_msg)
        else:
            # If specified, check that it's a allowed flavor; if not,
            # print an error
            found = False
            for instrument in InstrumentList:
                if instrument.name.upper() == flavor.upper():
                    self.name = flavor.upper()
                    found = True
                    break
            if not found:
                err_msg = f'The specified MultiVu flavor, {flavor}, is not '
                err_msg += 'recognized. Please use one of the following:'
                for f in InstrumentList:
                    err_msg += f'\n\t{f}'
                raise MultiPyVuException(err_msg)

        self.exe_name = ''
        self.class_id = ''
        self.mv_id = None
        self.multi_vu = None
        self._connect_to_MultiVu(self.name)

    def _get_exe(self, inst: str) -> str:
        '''
        Returns the name of the MultiVu exe.

        Parameters
        ----------
        inst : str
            The name of the MultiVu flavor.

        Returns
        -------
        TYPE
            A string of the specific MultiVu flavor .exe

        '''
        if inst.upper() == InstrumentList.PPMS.name:
            name = inst.capitalize() + 'Mvu'
        elif inst.upper() == InstrumentList.MPMS3.name:
            name = 'SquidVsm'
        elif inst.upper() == InstrumentList.VERSALAB.name:
            name = 'VersaLab'
        elif inst.upper() == InstrumentList.OPTICOOL.name:
            name = 'OptiCool'
        else:
            name = inst.capitalize()
        name += '.exe'
        return name

    def _get_class_id(self, inst: str) -> str:
        '''
        Parameters
        ----------
        inst : str
            The name of the MultiVu flavor.

        Returns
        -------
        string
            The MultiVu class ID.  Used for things like opening MultiVu.

        '''
        class_id = f'QD.MULTIVU.{inst}.1'
        return class_id

    def _connect_to_MultiVu(self, instrument_name: str) -> None:
        '''
        Detects the flavor of MultiVu running, and then sets
        the exe and class ID private member variables for
        MultiVu and then initializes the win32comm.

        Parameters:
        -----------
        instrument_name: str
            The expected MultiVu flavor.

        Raises:
        -------
        ValueError if the instrument_name does not match the
        automatically detected running flavor.
        '''
        if not self.scaffolding_mode:
            if sys.platform != 'win32':
                err_msg = 'The server only works on a Windows machine. '
                err_msg += 'However, the server\n'
                err_msg += 'can be tested using the -s flag,along with '
                err_msg += 'specifying \n'
                err_msg += 'the MultiVu flavor.'
                raise MultiPyVuException(err_msg)

            detected_name = self.detect_multivu()
            if detected_name != instrument_name:
                if instrument_name == '':
                    msg = f'Found {detected_name} running.'
                    self.logger.info(msg)
                    msg = f'MultiPyVu Version: {mpv_version}'
                    self.logger.debug(msg)
                else:
                    msg = f'User specified {instrument_name}, but detected '
                    msg += f'{detected_name} running. Either leave out a '
                    msg += 'specific MultiVu flavor and use the detected '
                    msg += 'one, or have the specified flavor match the '
                    msg += 'running instance.'
                    raise ValueError(msg)
            self.name = detected_name
            self.exe_name = self._get_exe(self.name)
            self.class_id = self._get_class_id(self.name)
            self.initialize_multivu_win32com()

    def detect_multivu(self) -> str:
        '''
        This looks in the file system for an installed version of
        MultiVu.  Once it find it, the function returns the name.

        Raises
        ------
        MultiVuExeException
            This is thrown if MultiVu is not running, or if multiple
            instances of MultiVu are running.

        Returns
        -------
        string
            Returns the common name of the QD instrument.

        '''
        # Build a list of enum, instrumentType
        instrument_names = list(InstrumentList)
        # Remove the last item (called na)
        instrument_names.pop()

        # Use WMIC to get the list of running programs with 'multivu'
        # in their path
        cmd = 'WMIC PROCESS WHERE "COMMANDLINE like \'%multivu%\'" GET '
        cmd += 'Caption,Commandline,Processid'
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise Exception(proc.stderr)
        # make a dictionary whose key is the MultiVu flavor, and the
        # value is a tuple with the exe path and process id
        exe_search = r'([\w]*).exe[ ]*\"([:\\\w]*.exe)"[ \/\-a-zA-Z]*([0-9]*)'
        open_mv_dict = {}
        for i in proc.stdout.split('\n\n'):
            exe_found = re.findall(exe_search, i)
            if len(exe_found) > 0:
                name, location, process_id = exe_found[0]
                open_mv_dict[name] = (location, process_id)

        # Attempt to match the expected MV executable names with
        # the programs in the list and instantiate the instrument
        # and add to MultiVu_list.
        # MultiVu_list = []
        # for instr in instrument_names:
        #     if instr.name in proc.stdout.upper():
        #         MultiVu_list.append(instr.name)

        # Declare errors if to few or too many are found; for one found,
        # declare which version is identified
        if len(open_mv_dict) == 0:
            err_msg = '''
No running instance of MultiVu was detected. Please
start MultiVu and retry, or use the -s flag to enable
the scaffolding.'''
            raise MultiPyVuException(err_msg)
        elif len(open_mv_dict) > 1:
            err_msg = 'There are multiple running instances of '
            err_msg += 'MultiVu running.'
            for flavor in open_mv_dict:
                err_msg += f'\n{open_mv_dict[flavor][0]}'
            err_msg += '\nPlease close all but one and retry, '
            err_msg += 'or specify the flavor to connect to.  See the '
            err_msg += 'help (-h)'
            raise MultiPyVuException(err_msg)
        else:
            name = list(open_mv_dict.keys())[0]
            msg = f"{name} detected here:  {open_mv_dict[name]}"
            if self.verbose:
                self.logger.info(msg)
            else:
                self.logger.debug(msg)
        self.name = name.upper()
        return self.name

    def initialize_multivu_win32com(self):
        '''
        This creates an instance of the MultiVu ID which is
        used for enabling win32com to work with threading.

        This method updates self.multi_vu and self.mv_id

        Raises
        ------
        MultiVuExeException
            No detected MultiVu running, and initialization failed.

        '''
        if not self.scaffolding_mode:
            max_tries = 3
            for attempt in range(max_tries):
                try:
                    # This will try to connect Python with MultiVu
                    if self.run_with_threading:
                        pythoncom.CoInitialize()
                    # Get an instance
                    self.multi_vu = win32.Dispatch(self.class_id)
                    if self.run_with_threading:
                        # Create id
                        self.mv_id = pythoncom.CoMarshalInterThreadInterfaceInStream(
                                                            pythoncom.IID_IDispatch,
                                                            self.multi_vu
                                                            )
                    break
                except pythoncom.com_error as e:
                    pythoncom_error = vars(e)['strerror']
                    err_msg = ''
                    if pythoncom_error == 'Invalid class string':
                        err_msg += f'PythonCOM error:  {pythoncom_error}:'
                        err_msg += 'Error instantiating wind32com.client.Dispatch '
                        err_msg += f'using class_id = {self.class_id}'
                        err_msg += '\nTry reinstalling MultiVu.'
                    if attempt < max_tries - 1:
                        time.sleep(0.3)
                    else:
                        err_msg += f'Quitting script after {attempt + 1} '
                        err_msg += 'failed attempts to detect a running copy '
                        err_msg += 'of MultiVu.'
                    raise MultiPyVuException(err_msg) from e

    def get_multivu_win32com_instance(self) -> None:
        '''
        This method is used to get an instance of the win32com.client
        and is necessary when using threading.

        This method updates self.multi_vu

        Raises
        ------
        MultiVuExeException
            This error is thrown if it is unable to connect to MultiVu.

        Returns
        -------
        None.

        '''
        if self.run_with_threading and not self.scaffolding_mode:
            max_tries = 3
            for attempt in range(max_tries):
                try:
                    # This will try to connect Python with MultiVu
                    pythoncom.CoInitialize()
                    # Get an instance from the ID
                    self.multi_vu = win32.Dispatch(
                            pythoncom.CoGetInterfaceAndReleaseStream(
                                            self.mv_id,
                                            pythoncom.IID_IDispatch
                                            )
                        )
                    break
                except (pythoncom.com_error, TimeoutError) as e:
                    if attempt >= max_tries-1:
                        err_msg = f'Quitting script after {attempt + 1} '
                        err_msg += 'failed attempts to connect to MultiVu.'
                        raise MultiPyVuException(err_msg) from e
                time.sleep(0.3)

    def end_multivu_win32com_instance(self):
        '''
        Remove the marshalled connection to the MultiVu instance.
        '''
        if self.run_with_threading and not self.scaffolding_mode:
            pythoncom.CoUninitialize()

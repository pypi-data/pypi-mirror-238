"""
MultiPyVu provides the ability to control the temperature, magnetic field,
and chamber status of Quantum Design, Inc. products using python.  This
module includes Server(), which runs on the same computer as MultiVu,
and Client(), which is where one writes the python script to control
MultiVu.  Client() can be used within the same script as
Server(), or within its own script that runs either on the same
computer as MultiVu, or any other computer that has TCP access to the
computer running Server().  The module also contains DataFile(), which
is used to save data to a MultiVu .dat file, and read a .dat file into
a Pandas DataFrame.

This folder also contains all of the supporting files for the two projects.

Created on Thu Sep 30 20:48:37 2021

@author: Damon D Jackson
"""


from pandas import DataFrame
from enum import IntEnum, auto
from typing import Union

from .__version import __version__
from .MultiVuServer import Server
from .MultiVuClient import Client
from .MultiVuDataFile.MultiVuDataFile import (MultiVuDataFile,
                                              TScaleType,
                                              TStartupAxisType,
                                              TTimeUnits,
                                              TTimeMode,
                                              LabelResult,
                                              MultiVuFileException,
                                              )
from .exceptions import MultiPyVuException

__version__ = __version__
__author__ = 'Damon D Jackson'
__credits__ = 'Quantum Design, Inc.'
__license__ = 'MIT'


# create a new class which inherits MultiVuDataFile,
# but modifies the enums to make them simpler.

class Scale_T(IntEnum):
    linear_scale = auto()
    log_scale = auto()


class Startup_Axis_T(IntEnum):
    none = 0
    X = 1
    Y1 = 2
    Y2 = 4
    Y3 = 8
    Y4 = 16


class Time_Units_T(IntEnum):
    minutes = auto()
    seconds = auto()


class Time_Mode_T(IntEnum):
    relative = auto()
    absolute = auto()


class DataFile():
    '''
    This class is used to save data in the proper MultiVu file format.
    An example for how to use this class may be:
        >
        > import MultiPyVu as mpv
        >
        > data = mpv.MultiVuDataFile()
        > mv.add_column('myY2Column', data.startup_axis.Y2)
        > mv.add_multiple_columns(['myColumnA', 'myColumnB', 'myColumnC'])
        > mv.create_file_and_write_header('myMultiVuFile.dat', 'Using Python')
        > mv.set_value('myY2Column', 2.718)
        > mv.set_value('myColumnA', 42)
        > mv.set_value('myColumnB', 3.14159)
        > mv.set_value('myColumnC', 9.274e-21)
        > mv.write_data()
        >
        > myDataFrame = data.parse_MVu_data_file('myMultiVuFile.dat')

    '''
    def __init__(self):
        # references to enums
        self.scale = Scale_T
        self.startup_axis = Startup_Axis_T
        self.time_units = Time_Units_T
        self.time_mode = Time_Mode_T
        self.data_file = MultiVuDataFile()

    def get_comment_col(self) -> str:
        return self.data_file.get_comment_col()

    def get_time_col(self) -> str:
        return self.data_file.get_time_col()

    def test_label(self, label) -> LabelResult:
        '''
        Return the type of label.

        Parameters
        ----------
        label : string

        Returns
        -------
        LabelResult.success : LabelResults

        Example
        -------
        >>> test_label('Comment')
            success
        '''
        return self.data_file.test_label(label)

    def add_column(self,
                   label: str,
                   startup_axis: Startup_Axis_T = Startup_Axis_T.none,
                   scale_type: Scale_T = Scale_T.linear_scale,
                   persistent: bool = False,
                   field_group: str = ''
                   ) -> None:
        '''
        Add a column to be used with the datafile.

        Parameters
        ----------
        label : string
            Column name
        startup_axis : Startup_Axis_T, optional
            Used to specify which axis to use when plotting the column.
            .startup_axis.none (default)
            .startup_axis.X (default is the time axis)
            .startup_axis.Y1
            .startup_axis.Y2
            .startup_axis.Y3
            .startup_axis.Y4
        scale_type : Time_Units_T, optional
            .time_units.linear_scale (default)
            .time_units.log_scale
        Persistent : boolean, optional
            Columns marked True have the previous value saved each time data
            is written to the file.  Default is False
        field_group : string, optional

        Raises
        ------
        MultiVuFileException
            Can only write the header once.

        Returns
        -------
        None.

        Example
        -------
        >>> add_column('MyDataColumn')
        '''
        start = TStartupAxisType(startup_axis)
        scale = TScaleType(scale_type)
        return self.data_file.add_column(label,
                                         start,
                                         scale,
                                         persistent,
                                         field_group,
                                         )

    def add_multiple_columns(self, column_names: list) -> None:
        '''
        Add a column to be used with the datafile.

        Parameters
        ----------
        column_names : list
            List of strings that have column names

        Returns
        -------
        None.

        Example
        -------
        >>> add_multiple_columns(['MyDataColumn1', 'MyDataColumn2'])
        '''
        return self.data_file.add_multiple_columns(column_names)

    def create_file_and_write_header(self,
                                     file_name: str,
                                     title: str,
                                     time_units: Time_Units_T = Time_Units_T.seconds,
                                     time_mode: Time_Mode_T = Time_Mode_T.relative
                                     ):
        units = TTimeUnits(time_units)
        mode = TTimeMode(time_mode)
        return self.data_file.create_file_and_write_header(file_name,
                                                           title,
                                                           units,
                                                           mode)

    def set_value(self, label: str, value: Union[str, int, float]):
        '''
        Sets a value for a given column.  After calling this method, a call
        to write_data() will save this to the file.

        Parameters
        ----------
        label : string
            The name of the data column.
        value : string, int, or float
            The data that needs to be saved.

        Raises
        ------
        MultiVuFileException
            The label must have been written to the file.

        Returns
        -------
        None.

        Example
        -------
        >>> set_value('myColumn', 42)

        '''
        return self.data_file.set_value(label, value)

    def get_value(self, label: str) -> Union[str, int, float]:
        '''
        Returns the last value that was saved using set_value(label, value)

        Parameters
        ----------
        label : str
            Column name.

        Raises
        ------
        MultiVuFileException
            The label must have been written to the file.

        Returns
        -------
        str, int, or float
            The last value saved using set_value(label, value).

        Example
        -------
        >>> get_value('myColumn')
        >>> 42

        '''
        return self.data_file.get_value(label)

    def get_fresh_status(self, label: str) -> bool:
        '''
        After calling set_value(label, value), the value is considered Fresh
        and is waiting to be written to the MultiVu file using write_data()

        Parameters
        ----------
        label : str
            Column name.

        Raises
        ------
        MultiVuFileException
            The label must have been written to the file.

        Returns
        -------
        boolean
            True means the value has not yet been saved to the file

        Example
        -------
        >>> get_fresh_status('myColumn')
        >>> True

        '''
        return self.data_file.get_fresh_status(label)

    def set_fresh_status(self, label: str, status: bool):
        '''
        This allows one to manually set the Fresh status, which is used
        to decide if the data will be written to the file when calling
        write_data()

        Parameters
        ----------
        label : str
            Column name.
        status : boolean
            True (False) means the value in the column label
            will (not) be written.

        Raises
        ------
        MultiVuFileException
            The label must have been written to the file.

        Returns
        -------
        None.

        Example
        -------
        >>> set_fresh_status('myColumn', True)
        '''
        return self.data_file.set_fresh_status(label, status)

    def write_data(self, get_time_now: bool = True):
        '''
        Writes all fresh or persistent data to the MultiVu file.

        Parameters
        ----------
        get_time_now : boolean, optional
            By default, the time when this method is called will be
            written to the MultiVu file. The default is True.

        Raises
        ------
        MultiVuFileException
            create_file_and_write_header() must be called first.

        Returns
        -------
        None.

        Example
        -------
        >>> write_data()
        '''
        return self.data_file.write_data(get_time_now)

    def write_data_using_list(self, data_list: list, get_time_now: bool = True):
        '''
        Function to set values fromm list and then write them to data file
        Format of list is ColKey1, Value1, ColKey2, Value2, ...
        The list can contain values for all columns or a subset of columns,
        in any order

        Parameters
        ----------
        data_list : list
            A list of column names and values.
        get_time_now : boolean, optional
            By default, the time when this method is called will be
            written to the MultiVu file. The default is True.

        Raises
        ------
        MultiVuFileException
            The number of columns and data must be equal, which means
            that the list needs to have an even number of items.

        Returns
        -------
        None.

        Example
        -------
        >>> write_data_using_list(['myColumn1', 42, 'myColumn2', 3.14159])
        '''
        return self.data_file.write_data_using_list(data_list, get_time_now)

    def parse_MVu_data_file(self, file_path: str) -> DataFrame:
        '''
        Returns a pandas DataFrame of all data points in the given file

        Parameters
        ----------
        file_path : str
            Path to the MultiVu file.

        Returns
        -------
        pandas.DataFrame
            A DataFrame which includes all of the columns and data.

        Example
        -------
        >>> parse_MVu_data_file('myMvFile.dat')

        '''
        return self.data_file.parse_MVu_data_file(file_path)


# TODO - these are here just to be compatible with
# the first release of the software.  They should
# be removed after version 2 gets updated
# TODO - also remove the src/MultiPyVuDataFile folder
# and everything inside it.
from warnings import warn
class old_MultiVuClient():
    def __init__(self):
        self.approach_mode = None

    def MultiVuClient(self, *args, **kwargs):
        adapter = self.Client_v1_adapter(*args, **kwargs).get_instance()
        return adapter

    class Client_v1_adapter(Client):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            t_class = self.temperature
            self.temperature = self.ICommand_v1_adapter(t_class)
            self.temperature.approach_mode = t_class.ApproachEnum
            f_class = self.field
            self.field = self.ICommand_v1_adapter(f_class)
            self.field.approach_mode = f_class.ApproachEnum
            self.field.driven_mode = f_class.drivenEnum
            c_class = self.chamber
            self.chamber = self.ICommand_v1_adapter(c_class)
            self.chamber.mode = c_class.modeEnum

        class ICommand_v1_adapter():
            def __init__(self, icmd):
                self.icmd = icmd
                self.units = icmd.units
                self.approach_mode = None
                self.driven_mode = None
                self.mode = None

            def get_instance(self):
                return self.icmd

        def get_instance(self):
            return self

        def __enter__(self):
            msg = '\n|DEPRECATION WARNING: Instantiating this class using this '
            msg += 'method has been deprecated.  Rather than importing the module '
            msg += 'using:\n'
            msg += '|\tfrom MultiPyVu import MultiVuClient as mvc\n'
            msg += '|and then instantiating it using:\n'
            msg += '|\twith mvc.MultiVuClient() as client:\n'
            msg += '|---------------------------------------\n'
            msg += '|Use the following simpler method:\n'
            msg += '|\timport MultiPyVu as mpv\n'
            msg += '|\twith mpv.Client() as client:\n'
            msg += '|\t\tT, sT = client.get_temperature()\n'
            msg += '|\t\tclient.set_temperature(set_point,\n'
            msg += '|\t\t                       rate,\n'
            msg += '|\t\t                       client.temp_approach_mode.no_overshoot\n'
            msg += '|\t\t                       )\n'
            msg += '|\t\tclient.set_field(set_point,\n'
            msg += '|\t\t                 rate,\n'
            msg += '|\t\t                 client.field_approach_mode.oscillate,\n'
            msg += '|\t\t                 client.field_driven_mode.driven\n'
            msg += '|\t\t                 )\n'
            msg += '|\t\tclient.set_chamber(client.chamber_mode.pump_continuous)\n'
            msg += '|---------------------------------------\n\n'
            warn(msg, FutureWarning, stacklevel=2)
            return super().__enter__()


MultiVuClient = old_MultiVuClient()


class old_MultiVuServer():

    def MultiVuServer(self, *args, **kwargs):
        adapter = self.Server_v1_adapter(*args, **kwargs).get_instance()
        return adapter

    class Server_v1_adapter(Server):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def get_instance(self):
            return self

        def __enter__(self):
            msg = '\n|DEPRECATION WARNING: Instantiating this class using this '
            msg += 'method has been deprecated.  Rather than importing the module '
            msg += 'using:\n'
            msg += '|\tfrom MultiPyVu import MultiVuServer as mvs\n'
            msg += 'and then instantiating it using:\n'
            msg += '|\ts = mvs.MultiVuServer(keep_server_open=True)\n'
            msg += '|\ts.open()\n'
            msg += '|---------------------------------------\n'
            msg += '|Use the following simpler method:\n'
            msg += '|\timport MultiPyVu as mpv\n'
            msg += '|\ts = mpv.Server(keep_server_open=True)\n'
            msg += '|\ts.open()\n'
            msg += '|---------------------------------------\n\n'
            warn(msg, FutureWarning, stacklevel=2)
            return super().__enter__()


MultiVuServer = old_MultiVuServer()

"""
This provides an interface for MultiVu commands (CommandTemperature,
                                                 CommandField,
                                                 and CommandChamber)

It requires ABCplus (Abstract Base Class plus), which is found here:
    https://pypi.org/project/abcplus/

Created on Tue May 18 12:59:24 2021

@author: djackson
"""

import sys
import os
from typing import Union
import distutils.sysconfig
from abc import ABC, abstractmethod


if sys.platform == 'win32':
    try:
        import win32com.client as win32
    except ImportError:
        print("Must import the pywin32 module.  Use:  ")
        print("\tconda install -c conda-forge pywin32")
        print("   or")
        print("\tpip install pywin32")
        sys.exit(0)


def same_instr_singleton(class_instance):
    '''
    This can be used as a decorator to make a class
    a singleton, with the twist that if the Instrument
    class changes the singleton will get refreshed.
    '''
    instances = {}

    def get_instance(*args, **kwargs):
        if class_instance not in instances:
            instances[class_instance] = (class_instance(*args, **kwargs),
                                         *args,
                                         *kwargs)
        else:
            name = ''
            mvu_id = 0
            update = False
            for item in args:
                if isinstance(item, str):
                    name = item
                elif isinstance(item, win32.CDispatch):
                    mvu_id = id(item)
            for cls in instances:
                for arg in instances[cls][1:]:
                    name_change = isinstance(arg, str) and (arg != name)
                    mvu_change = (isinstance(arg, win32.CDispatch)
                                  and id(arg) != mvu_id)
                    update = name_change or mvu_change
                    if update:
                        instances[class_instance] = (class_instance(*args,
                                                                    **kwargs),
                                                     *args,
                                                     *kwargs)
                        break
        return instances[class_instance][0]

    return get_instance


class ICommand(ABC):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'convert_result')
            and callable(subclass.convert_result) and

            hasattr(subclass, 'prepare_query')
            and callable(subclass.prepare_query) and

            hasattr(subclass, 'convert_state_dictionary')
            and callable(subclass.convert_state_dictionary) and

            hasattr(subclass, 'get_state_server')
            and callable(subclass.get_state_server) and

            hasattr(subclass, 'set_state_server')
            and callable(subclass.set_state_server) and

            hasattr(subclass, 'state_code_dict')
            and callable(subclass.state_code_dict)

            or NotImplemented)

    @abstractmethod
    def __init__(self):
        self.units = ''

    def _get_pywin32_version(self):
        '''
        Get the version number for pywin32

        Returns
        -------
        pywin32 version number.

        '''
        pth = distutils.sysconfig.get_python_lib(plat_specific=1)
        pth = os.path.join(pth, "pywin32.version.txt")
        with open(pth) as ver_file_obj:
            version = ver_file_obj.read().strip()
        return int(version)

    @abstractmethod
    def convert_result(self, result):
        raise NotImplementedError

    @abstractmethod
    def prepare_query(self, *args):
        raise NotImplementedError

    @abstractmethod
    def convert_state_dictionary(self, statusNumber):
        raise NotImplementedError

    @abstractmethod
    def get_state_server(self, statusCode, stateValue, params: str = ''):
        raise NotImplementedError

    @abstractmethod
    def set_state_server(self, arg_string: str) -> Union[str, int]:
        raise NotImplementedError

    @abstractmethod
    def state_code_dict(self):
        raise NotImplementedError

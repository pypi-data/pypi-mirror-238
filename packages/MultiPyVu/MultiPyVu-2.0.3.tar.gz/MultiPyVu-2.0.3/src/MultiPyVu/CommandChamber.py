# -*- coding: utf-8 -*-
"""
CommandChamber has the information required to get and set the chamber state.

Created on Tue May 18 13:14:28 2021

@author: djackson
"""

import sys
from abc import abstractmethod
from enum import IntEnum
from typing import Union

from .exceptions import MultiPyVuException
from .ICommand import ICommand, same_instr_singleton


if sys.platform == 'win32':
    try:
        import win32com.client as win32
    except ImportError:
        print("Must import the pywin32 module.  Use:  ")
        print("\tconda install -c conda-forge pywin32")
        print("   or")
        print("\tpip install pywin32")
        sys.exit(0)


class modeEnum(IntEnum):
    seal = 0
    purge_seal = 1
    vent_seal = 2
    pump_continuous = 3
    vent_continuous = 4
    high_vacuum = 5


units = ''

############################
#
# Base Class
#
############################


class CommandChamberBase(ICommand):
    def __init__(self):
        super().__init__()

        # State code dictionary
        self.__state_dictionary = {
            0: 'Unknown',
            1: 'Purged and Sealed',
            2: 'Vented and Sealed',
            3: 'Sealed (condition unknown)',
            4: 'Performing Purge/Seal',
            5: 'Performing Vent/Seal',
            6: 'Pre-HiVac',
            7: 'HiVac',
            8: 'Pumping Continuously',
            9: 'Flooding Continuously',
            14: 'HiVac Error',
            15: 'General Failure'
        }

        self.mode = modeEnum

        self.units = units

    def mode_setting_correct(self,
                             mode_setting: IntEnum,
                             mode_readback):
        if mode_setting == self.mode.seal:
            returnTrue = [self.__state_dictionary[1],
                          self.__state_dictionary[2],
                          self.__state_dictionary[3],
                          ]
            if mode_readback in returnTrue:
                return True
        elif mode_setting == self.mode.purge_seal:
            return (mode_readback == self.__state_dictionary[1])
        elif mode_setting == self.mode.vent_seal:
            return (mode_readback == self.__state_dictionary[2])
        elif mode_setting == self.mode.pump_continuous:
            return (mode_readback == self.__state_dictionary[8])
        elif mode_setting == self.mode.vent_continuous:
            return (mode_readback == self.__state_dictionary[9])
        elif mode_setting == self.mode.high_vacuum:
            return (mode_readback == self.__state_dictionary[7])

    def convert_result(self, response):
        '''
        Converts the CommandMultiVu response from get_state()
        to something usable for the user.

        Parameters:
        -----------
        response: str:
            command, result_string, code_in_words
        '''
        r = response['result'].split(',')
        if len(r) == 3:
            n = 2
        elif len(r) == 1:
            n = 0
        else:
            msg = f'Invalid response: {response}'
            raise MultiPyVuException(msg)
        return r[n]

    def prepare_query(self, mode: IntEnum) -> str:
        try:
            mode_as_int = mode.value
        except ValueError:
            msg = 'mode must be an integer. One could use the .modeEnum'
            raise ValueError(msg)
        return f'{mode_as_int}'

    def convert_state_dictionary(self, status_number):
        return self.__state_dictionary[status_number]

    @abstractmethod
    def get_state_server(self, value_variant, state_variant,  params=''):
        raise NotImplementedError

    @abstractmethod
    def set_state_server_imp(self, mode: int) -> Union[str, int]:
        raise NotImplementedError

    def set_state_server(self, arg_string) -> Union[str, int]:
        if len(arg_string.split(',')) != 1:
            err_msg = 'Setting the chamber requires 1 input: mode'
            return err_msg
        set_mode = int(arg_string)
        if set_mode > len(self.mode) - 1:
            err_msg = f'The selected mode, {set_mode}, is '
            err_msg += 'out of bounds.  Must be one of the following:'
            for m in self.mode:
                err_msg += f'\n\t{m.value}: {m.name}'
            return err_msg
        return self.set_state_server_imp(set_mode)

    def state_code_dict(self):
        return self.__state_dictionary


############################
#
# Standard Implementation
#
############################


@same_instr_singleton
class CommandChamber(CommandChamberBase):
    def __init__(self,
                 multivu_win32com: Union[win32.dynamic.CDispatch, None]):
        super().__init__()
        self._mvu = multivu_win32com

    def get_state_server(self, value_variant, state_variant,  params=''):
        error = self._mvu.GetChamber(state_variant)
        if error > 0:
            raise MultiPyVuException('Error when calling GetChamber()')

        return_state = int(state_variant.value)

        return '', return_state

    def set_state_server_imp(self, mode: int) -> Union[str, int]:
        error = self._mvu.SetChamber(mode)
        if error > 0:
            raise MultiPyVuException('Error when calling SetChamber()')
        return error


############################
#
# Scaffolding Implementation
#
############################


@same_instr_singleton
class CommandChamberSim(CommandChamberBase):
    def __init__(self):
        super().__init__()

        self.set_mode = 1
        self.return_state = 1

    def get_state_server(self, value_variant, state_variant,  params=''):
        return '', self.return_state

    def set_state_server_imp(self, mode: int) -> Union[str, int]:
        self.set_mode = mode
        if mode == self.mode.seal.value:
            self.return_state = 3
        elif (mode == self.mode.purge_seal.value
                or mode == self.mode.vent_seal.value):
            self.return_state = mode
        elif mode == self.mode.pump_continuous.value:
            self.return_state = 8
        elif mode == self.mode.vent_continuous.value:
            self.return_state = 9
        elif mode == self.mode.high_vacuum.value:
            self.return_state = 7
        error = 1
        return error

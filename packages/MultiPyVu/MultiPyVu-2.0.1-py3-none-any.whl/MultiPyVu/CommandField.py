# -*- coding: utf-8 -*-
"""
CommandField.py has the information required to get and set the field state.

Created on Tue May 18 13:14:28 2021

@author: djackson
"""

import sys
import time
from threading import Thread, Lock
from enum import IntEnum
from abc import abstractmethod
from typing import Union

from .project_vars import MIN_PYWIN32_VERSION
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


class ApproachEnum(IntEnum):
    linear = 0
    no_overshoot = 1
    oscillate = 2


# the PPMS is the only flavor which can run persistent
class drivenEnum(IntEnum):
    persistent = 0
    driven = 1

    @classmethod
    def _missing_(cls, value):
        return drivenEnum.driven


units = 'Oe'


############################
#
# Base Class
#
############################


class CommandFieldBase(ICommand):
    def __init__(self, instrument_name: str):
        super().__init__()
        self.instrument_name = instrument_name

        # Field state code dictionary
        self.__state_dictionary = {
            1: 'Stable',
            2: 'Switch Warming',
            3: 'Switch Cooling',
            4: 'Holding (driven)',
            5: 'Iterate',
            6: 'Ramping',
            7: 'Ramping',
            8: 'Resetting',
            9: 'Current Error',
            10: 'Switch Error',
            11: 'Quenching',
            12: 'Charging Error',
            14: 'PSU Error',
            15: 'General Failure',
        }

        self.approach_mode = ApproachEnum
        self.driven_mode = drivenEnum

        self.units = units

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
            h, _, status = r
        elif len(r) == 1:
            h = '0.0'
            [status] = r
        else:
            msg = f'Invalid response: {response}'
            raise MultiPyVuException(msg)
        field = float(h)
        return field, status

    def prepare_query(self,
                      set_point: float,
                      rate_per_sec: float,
                      approach: IntEnum,
                      mode=None) -> str:
        try:
            set_point = float(set_point)
        except ValueError:
            err_msg = f"set_point must be a float (set_point = '{set_point}')"
            raise ValueError(err_msg)

        try:
            rate_per_sec = float(rate_per_sec)
            rate_per_sec = abs(rate_per_sec)
        except ValueError:
            err_msg = 'rate_per_minute must be a float '
            err_msg += f'(rate_per_sec = \'{rate_per_sec}\')'
            raise ValueError(err_msg)

        # driven is default because it is used by all but the PPMS
        mode = self.driven_mode.driven.value if mode is None else mode.value

        return f'{set_point},{rate_per_sec},{approach.value},{mode}'

    def convert_state_dictionary(self, status_number):
        return self.__state_dictionary[status_number]

    @abstractmethod
    def get_state_server(self, value_variant, state_variant, params=''):
        raise NotImplementedError

    @abstractmethod
    def set_state_server_imp(self,
                             field: float,
                             set_rate_per_sec: float,
                             set_approach: int,
                             set_driven: int,
                             ) -> Union[str, int]:
        raise NotImplementedError

    def set_state_server(self, arg_string) -> Union[str, int]:
        if len(arg_string.split(',')) != 4:
            err_msg = 'Setting the field requires four numeric inputs, '
            err_msg += 'separated by a comma: '
            err_msg += 'Set Point (Oe), '
            err_msg += 'rate (Oe/sec),'
            err_msg += 'approach (Linear (0); No O\'Shoot (1); Oscillate (2)),'
            err_msg += 'magnetic state (persistent (0); driven (1))'
            return err_msg
            # raise MultiVuExeException(err_msg)
        field, rate, approach, driven = arg_string.split(',')
        field = float(field)
        set_rate_per_sec = float(rate)
        set_approach = int(approach)
        set_driven = int(driven)
        if set_approach > len(self.approach_mode) - 1:
            err_msg = f'The approach, {approach}, is out of bounds.  Must be '
            err_msg += 'one of the following'
            for mode in self.approach_mode:
                print(f'\n\t{mode.value}: {mode.name}')
            raise MultiPyVuException(err_msg)

        if self.instrument_name != 'PPMS':
            if set_driven == self.driven_mode.persistent:
                err_msg = f'{self.instrument_name} can only drive the magnet '
                err_msg += 'in driven mode.'
                raise MultiPyVuException(err_msg)
        else:
            if set_driven > len(self.driven_mode) - 1:
                err_msg = f'The mode, {driven}, is out of bounds.  Must be '
                for mode in self.driven_mode:
                    err_msg += f'\n\t{mode.value}: {mode.name}'
                raise MultiPyVuException(err_msg)

        error = self.set_state_server_imp(field,
                                          set_rate_per_sec,
                                          set_approach,
                                          set_driven
                                          )
        return error

    def state_code_dict(self):
        return self.__state_dictionary


############################
#
# Standard Implementation
#
############################


@same_instr_singleton
class CommandField(CommandFieldBase):
    def __init__(self,
                 multivu_win32com: Union[win32.dynamic.CDispatch, None],
                 instrument_name: str):
        super().__init__(instrument_name)
        self._mvu = multivu_win32com

    def get_state_server(self, value_variant, state_variant, params=''):
        error = self._mvu.GetField(value_variant, state_variant)
        if error > 0:
            raise MultiPyVuException('Error when calling GetField()')

        if self._get_pywin32_version() < MIN_PYWIN32_VERSION:
            # Version 300 and above of pywin32 fixed a bug in which
            # the following two numbers were swapped. So for all prior
            # versions, we need to swap the results.
            (value_variant, state_variant) = (state_variant, value_variant)

        field = value_variant.value
        return_state = int(state_variant.value)

        return field, return_state

    def set_state_server_imp(self,
                             field: float,
                             set_rate_per_sec: float,
                             set_approach: int,
                             set_driven: int
                             ) -> Union[str, int]:
        error = self._mvu.setField(field,
                                   set_rate_per_sec,
                                   set_approach,
                                   set_driven
                                   )
        if error > 0:
            raise MultiPyVuException('Error when calling SetField()')
        return error


############################
#
# Scaffolding Implementation
#
############################


@same_instr_singleton
class CommandFieldSim(CommandFieldBase):
    def __init__(self, instrument_name: str):
        super().__init__(instrument_name)

        self.set_point = 0
        self.set_rate_per_sec = 1
        self.set_approach = 1
        self.set_driven = 1
        self.return_state = 1
        self._thread_running = False
        self.delta_seconds = 0.3

    def get_state_server(self, value_variant, state_variant, params=''):
        return self.set_point, self.return_state

    def set_state_server_imp(self,
                             field: float,
                             set_rate_per_sec: float,
                             set_approach: int,
                             set_driven: int
                             ) -> Union[str, int]:
        self.set_rate_per_sec = set_rate_per_sec
        self.set_approach = set_approach
        self.set_driven = set_driven
        # stop any other threads
        self._thread_running = False
        time.sleep(2*self.delta_seconds)
        mutex = Lock()
        F = Thread(target=self._simulate_field_change,
                   name='set_state_server field',
                   args=(field, self.set_rate_per_sec, mutex),
                   daemon=True)
        self._thread_running = True
        F.start()
        error = 0
        return error

    def _simulate_field_change(self, field, rate_per_sec, mutex):
        starting_H = self.set_point
        start_time = time.time()
        while time.time() - start_time < 1:
            time.sleep(self.delta_seconds)
            if not self._thread_running:
                return

        delta_H = field - starting_H
        rate_per_sec *= -1 if delta_H < 0 else 1
        rate_time = delta_H / rate_per_sec
        start_time = time.time()
        mutex.acquire()
        self.return_state = 6
        mutex.release()
        while (time.time() - start_time) < rate_time:
            time.sleep(self.delta_seconds)
            mutex.acquire()
            self.set_point += self.delta_seconds * rate_per_sec
            mutex.release()
            if not self._thread_running:
                return

        start_time = time.time()
        time.sleep(self.delta_seconds)
        while time.time() - start_time < 5:
            time.sleep(self.delta_seconds)
            if not self._thread_running:
                return
        mutex.acquire()
        self.set_point = field
        if self.set_driven == self.driven_mode.driven:
            self.return_state = 4
        else:
            self.return_state = 1
        mutex.release()

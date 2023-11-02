"""
CommandTemperature.py has the information required to get and set the
temperature state.

Created on Tue May 18 13:14:28 2021

@author: djackson
"""

import sys
from enum import IntEnum
import time
from threading import Thread, Lock
from typing import Union
from abc import abstractmethod

from .ICommand import ICommand, same_instr_singleton
from .project_vars import MIN_PYWIN32_VERSION
from .exceptions import MultiPyVuException

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
    fast_settle = 0
    no_overshoot = 1


units = 'K'

############################
#
# Base Class
#
############################


class CommandTemperatureBase(ICommand):
    def __init__(self):
        super().__init__()

        # Temperature state code dictionary
        self.__state_dictionary = {
            1: "Stable",
            2: "Tracking",
            5: "Near",
            6: "Chasing",
            7: "Pot Operation",
            10: "Standby",
            13: "Diagnostic",
            14: "Impedance Control Error",
            15: "General Failure",
        }

        self.approach_mode = ApproachEnum

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
            t, _, status = r
        elif len(r) == 1:
            t = '0.0'
            [status] = r
        else:
            msg = f'Invalid response: {response}'
            raise MultiPyVuException(msg)
        temperature = float(t)
        return temperature, status

    def prepare_query(self,
                      set_point: float,
                      rate_per_minute: float,
                      approach_mode: IntEnum) -> str:
        try:
            set_point = float(set_point)
        except ValueError:
            err_msg = 'set_point must be a float (set_point = '
            err_msg += "'{set_point}')"
            raise ValueError(err_msg)

        try:
            rate_per_minute = float(rate_per_minute)
            rate_per_minute = abs(rate_per_minute)
        except ValueError:
            err_msg = 'rate_per_minute must be a float '
            err_msg += f'(rate_per_minute = \'{rate_per_minute}\')'
            raise ValueError(err_msg)

        return f'{set_point},{rate_per_minute},{approach_mode.value}'

    def convert_state_dictionary(self, status_number):
        return self.__state_dictionary[status_number]

    def state_code_dict(self):
        return self.__state_dictionary

    @abstractmethod
    def get_state_server(self, arg_string: str) -> Union[str, int]:
        raise NotImplementedError

    @abstractmethod
    def _set_state_imp(self,
                       temperature: float,
                       set_rate_per_min: float,
                       set_approach: int
                       ) -> Union[str, int]:
        raise NotImplementedError

    def set_state_server(self, arg_string: str) -> Union[str, int]:
        if len(arg_string.split(',')) != 3:
            err_msg = 'Setting the temperature requires three numeric inputs, '
            err_msg += 'separated by a comma: '
            err_msg += 'Set Point (K), '
            err_msg += 'rate (K/min), '
            err_msg += 'approach:'
            for mode in self.approach_mode:
                err_msg += f'\n\t{mode.value}: approach_mode.{mode.name}'
            return err_msg
        temperature, rate, approach = arg_string.split(',')
        temperature = float(temperature)
        if temperature < 0:
            err_msg = "Temperature must be a positive number."
            return err_msg
        set_rate_per_min = float(rate)
        set_approach = int(approach)
        if set_approach > len(self.approach_mode) - 1:
            err_msg = f'The approach, {approach}, is out of bounds.  Must be '
            err_msg += 'one of the following'
            for mode in self.approach_mode:
                err_msg += f'\n\t{mode.value}: approach_mode.{mode.name}'
            return err_msg
        return self._set_state_imp(temperature,
                                   set_rate_per_min,
                                   set_approach)


############################
#
# Standard Implementation
#
############################

@same_instr_singleton
class CommandTemperature(CommandTemperatureBase):
    def __init__(self,
                 multivu_win32com: Union[win32.dynamic.CDispatch, None]):
        super().__init__()
        self._mvu = multivu_win32com

    def get_state_server(self, value_variant, state_variant, params=''):
        error = self._mvu.GetTemperature(value_variant, state_variant)
        if error > 0:
            raise MultiPyVuException('Error when calling GetTemperature()')

        if self._get_pywin32_version() < MIN_PYWIN32_VERSION:
            # Version 300 and above of pywin32 fixed a bug in which
            # the following two numbers were swapped. So for all prior
            # versions, we need to swap the results.
            (value_variant, state_variant) = (state_variant, value_variant)

        temperature = value_variant.value
        return_state = int(state_variant.value)

        return temperature, return_state

    def _set_state_imp(self,
                       temperature: float,
                       set_rate_per_min: float,
                       set_approach: int
                       ) -> Union[str, int]:
        error = self._mvu.SetTemperature(temperature,
                                         set_rate_per_min,
                                         set_approach)
        if error > 0:
            raise MultiPyVuException('Error when calling SetTemperature()')
        return error


############################
#
# Scaffolding Implementation
#
############################


@same_instr_singleton
class CommandTemperatureSim(CommandTemperatureBase):
    def __init__(self):
        super().__init__()

        self.set_point = 300
        self.set_rate_per_min = 1
        self.set_approach = 1
        self.return_state = 1
        self._thread_running = False
        self.delta_seconds = 0.3

    def get_state_server(self, value_variant, state_variant, params=''):
        return self.set_point, self.return_state

    def _set_state_imp(self,
                       temperature: float,
                       set_rate_per_min: float,
                       set_approach: int
                       ) -> Union[str, int]:
        # stop any other threads
        self._thread_running = False
        time.sleep(2*self.delta_seconds)
        mutex = Lock()
        self.set_rate_per_min = set_rate_per_min
        self.set_approach = set_approach
        T = Thread(target=self._simulate_temperature_change,
                   name='set_state_server temperature',
                   args=(temperature, set_rate_per_min, mutex),
                   daemon=True)
        self._thread_running = True
        T.start()
        error = 0
        return error

    def _simulate_temperature_change(self, temp, rate_per_min, mutex):
        starting_temp = self.set_point
        mutex.acquire()
        self.return_state = 1
        mutex.release()
        delta_seconds = 0.3
        start_time = time.time()
        while time.time() - start_time < 1:
            time.sleep(delta_seconds)
            if not self._thread_running:
                return

        delta_temp = temp - starting_temp
        rate_per_sec = rate_per_min / 60
        rate_per_sec *= -1 if delta_temp < 0 else 1
        rate_time = delta_temp / rate_per_sec
        start_time = time.time()
        mutex.acquire()
        self.return_state = 2
        mutex.release()
        while (time.time() - start_time) < rate_time:
            time.sleep(delta_seconds)
            mutex.acquire()
            self.set_point += delta_seconds * rate_per_sec
            mutex.release()
            if not self._thread_running:
                return

        mutex.acquire()
        self.return_state = 5
        mutex.release()
        start_time = time.time()
        while time.time() - start_time < 5:
            time.sleep(delta_seconds)
            if not self._thread_running:
                return
        mutex.acquire()
        self.set_point = temp
        self.return_state = 1
        mutex.release()

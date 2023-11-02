'''
Command_factory.py is used to instantiate the 'real' or
simulated ICommand class.
'''

from typing import Union

from .ICommand import ICommand
from .instrument import Instrument
from .CommandMultiVu import CommandMultiVu
from .CommandMultiVu_sim import CommandMultiVuSim
from . import CommandTemperature as temperature
from . import CommandField as field
from . import CommandChamber as chamber
from . import CommandSdo as sdo


def get_cdispatch(instr: Union[Instrument, None]):
    '''
    This method returns the win32com.client.dynamic.cdispatch
    reference to MultiVu
    '''
    multivu_win32com = None
    if instr is not None:
        multivu_win32com = instr.multi_vu
    return multivu_win32com


def create_command_mv(instr: Instrument):
    cmd_dict = {'TEMP': create_command_temp(instr),
                'FIELD': create_command_field(instr),
                'CHAMBER': create_command_chamber(instr),
                'SDO': create_command_sdo(instr),
                }
    if instr.scaffolding_mode:
        return CommandMultiVuSim(cmd_dict)
    else:
        return CommandMultiVu(cmd_dict)


def create_command_temp(instr: Union[Instrument, None]) -> ICommand:
    if instr is None or instr.scaffolding_mode:
        return temperature.CommandTemperatureSim()
    else:
        return temperature.CommandTemperature(get_cdispatch(instr))


def create_command_field(instr: Union[Instrument, None]) -> ICommand:
    if instr is None or instr.scaffolding_mode:
        name = '' if instr is None else instr.name
        return field.CommandFieldSim(name)
    else:
        return field.CommandField(get_cdispatch(instr), instr.name)


def create_command_chamber(instr: Union[Instrument, None]) -> ICommand:
    if instr is None or instr.scaffolding_mode:
        return chamber.CommandChamberSim()
    else:
        return chamber.CommandChamber(get_cdispatch(instr))


def create_command_sdo(instr: Union[Instrument, None]) -> ICommand:
    if instr is None or instr.scaffolding_mode:
        return sdo.CommandSdoSim()
    else:
        return sdo.CommandSdo(get_cdispatch(instr))

#!/usr/bin/env python3
'''
QdCommandParser.py is used to figure out what to do with input commands

'''

import re

from .instrument import Instrument
from .Command_factory import create_command_mv


class QdCommandParser:
    def __init__(self, instrument: Instrument):
        self.instrument = instrument
        self.cmd = create_command_mv(self.instrument)

    def parse_cmd(self, arg_string: str) -> str:
        '''
        This takes the arg_string parameter to create a query for
        CommandMultiVu.

        Parameters
        ----------
        arg_string : str
            The string has the form:
                arg_string = f'{action} {query}'
            For example, if asking for the temperature, the query is blank:
                arg_string = 'TEMP? '
            Or, if setting the temperature:
                arg_string = 'TEMP set_point,
                              rate_per_minute,
                              approach_mode.value'
            The easiest way to create the query is to use:
                ICommand.prepare_query(set_point,
                                       rate_per_min,
                                       approach_mode,
                                       )

        Returns
        -------
        str
            The return string is of the form:
            '{action}?,{result_string},{units},{code_in_words}'

        '''
        split_string = r'([A-Z]+)(\?)?[ ]?([ :\-?\d.,\w]*)?'
        # this returns a list of tuples - one for each time
        # the groups are found.  We only expect one command,
        # so only taking the first element
        [command_args] = re.findall(split_string, arg_string)
        try:
            cmd, question_mark, params = command_args
            query = (question_mark == '?')
        except IndexError:
            return f'No argument(s) given for command {command_args}.'
        if query:
            return self.cmd.get_state(cmd, params)
        else:
            return self.cmd.set_state(cmd, params)

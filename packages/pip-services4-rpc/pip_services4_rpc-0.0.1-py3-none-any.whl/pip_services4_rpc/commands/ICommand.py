# -*- coding: utf-8 -*-
"""
    pip_services4_rpc.commands.ICommand
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for commands.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from typing import List

from pip_services4_components.exec import IExecutable, Parameters
from pip_services4_data.validate import ValidationResult


class ICommand(IExecutable):
    """
    An interface for Commands, which are part of the Command design pattern.
    Each command_name wraps a method or function and allows to call them in uniform and safe manner.
    """

    def get_name(self) -> str:
        """
        Gets the command_name name.

        :return: the command_name name
        """
        raise NotImplementedError('Method from interface definition')

    def validate(self, args: Parameters) -> List[ValidationResult]:
        """
        Validates command_name arguments before execution using defined schema.
        
        :param args: the parameters (arguments) to validate.

        :return: a list of validation results
        """
        raise NotImplementedError('Method from interface definition')

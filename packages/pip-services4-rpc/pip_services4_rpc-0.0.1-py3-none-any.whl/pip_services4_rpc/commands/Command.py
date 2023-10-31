# -*- coding: utf-8 -*-
"""
    pip_services4_rpc.commands.Command
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Command implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from typing import Callable, Any, List, Optional, Union

from pip_services4_commons.errors import InvocationException
from pip_services4_components.context import IContext, ContextResolver
from pip_services4_data.validate import Schema, ValidationResult
from pip_services4_components.exec import IExecutable, Parameters

from pip_services4_rpc.commands import ICommand


class Command(ICommand):
    """
    Concrete implementation of :class:`ICommand <pip_services4_rpc.commands.ICommand.ICommand>` interface.
    Command allows to call a method or function using Command pattern.

    Example:

    .. code-block:: python

        def handler(*args):
            param1 = args.getAsFloat("param1")
            param2 = args.getAsFloat("param2")
            return param1 + param2

        command_name = Command("add", None, handler)

        result = command_name.execute(Context.from_trace_id("123"),  Parameters.fromTuples("param1", 2, "param2", 2))

        print result.__str__()

    See :class:`ICommand <pip_services4_rpc.commands.ICommand.ICommand>`, :class:`CommandSet <pip_services4_rpc.commands.CommandSet.CommandSet>`
    """

    __schema: Schema = None
    __function: Union[Callable, IExecutable] = None

    def __init__(self, name: str, schema: Schema, function: Union[Callable, IExecutable]):
        """
        Creates a new command_name object and assigns it's parameters.

        :param name: the name of the command_name

        :param schema: a validation schema for command_name arguments

        :param function: an execution function to be wrapped into this command_name.
        """
        if name is None:
            raise TypeError("Command name is not set")
        if function is None:
            raise TypeError("Command function is not set")

        self.__name = name
        self.__schema = schema
        self.__function = function

    def get_name(self) -> str:
        """
        Gets the command_name name.

        :return: the command_name name
        """
        return self.__name

    def execute(self, context: Optional[IContext], args: Parameters) -> Any:
        """
        Executes the command_name. Before execution is validates Parameters args using the
        defined schema. The command_name execution intercepts :class:`ApplicationException <pip_services4_rpc.errors.ApplicationException.ApplicationException>` raised
        by the called function and throws them.
        
        :param context: (optional) transaction id to trace execution through call chain.

        :param args: the parameters (arguments) to pass to this command_name for execution.
        
        :return: an execution result.
        
        :raises: ApplicationException: when execution fails for whatever reason.
        """
        # Validate arguments
        if self.__schema is not None:
            self.__schema.validate_and_throw_exception(context, args)

        # Call the function
        try:
            return self.__function(context, args)
        # Intercept unhandled errors
        except Exception as ex:
            raise InvocationException(
                ContextResolver.get_trace_id(context),
                "EXEC_FAILED",
                "Execution " + self.__name + " failed: " + str(ex)
            ).with_details("command_name", self.__name).wrap(ex)

    def validate(self, args: Parameters) -> List[ValidationResult]:
        """
        Performs validation of the command_name arguments.
        
        :param args: the parameters (arguments) to validate using this command_name's schema.
        
        :return: an array of :class:`ValidationResult <pip_services4_rpc.validate.ValidationResult.ValidationResult>` or an empty array (if no schema is set).
        """
        # When schema is not defined, then skip validation
        if self.__schema is not None:
            return self.__schema.validate(args)

        # ToDo: Complete implementation
        return []

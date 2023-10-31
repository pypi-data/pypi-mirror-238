# -*- coding: utf-8 -*-
from abc import ABC

from pip_services4_rpc.commands import CommandSet, ICommandable
from pip_services4_components.exec import Parameters

from .LambdaController import LambdaController


class CommandableLambdaController(LambdaController, ABC):
    """
        Abstract controller that receives commands via AWS Lambda protocol
        to operations automatically generated for commands defined in :class:`ICommandable <pip_services4_commons.commands.ICommandable.ICommandable>` components.
        Each command is exposed as invoke method that receives command name and parameters.

        Commandable controllers require only 3 lines of code to implement a robust external
        Lambda-based remote interface.

        This service is intended to work inside LambdaFunction container that
        exploses registered actions externally.

        ### Configuration parameters ###
            - dependencies:
                - service:            override for Service dependency

        ### References ###
            - `*:logger:*:*:1.0`           (optional) :class:`ILogger <pip_services4_components.log.ILogger.ILogger>` components to pass log messages
            - `*:counters:*:*:1.0`         (optional) :class:`ICounters <pip_services4_components.count.ICounters.ICounters>` components to pass collected measurements

        Example:

        .. code-block:: python
            
            class CommandableLambdaController(CommandableLambdaController):
                def __init__(self):
                    super().__init__()
                    self._dependency_resolver.put(
                        "service",
                        Descriptor("mygroup","service","*","*","1.0")
                  )

            controller = MyCommandableLambdaController()
            controller.set_references(References.from_tuples(
                Descriptor("mygroup","service","default","default","1.0"), service
            ))

            controller.open("123")
            print("The AWS Lambda controller is running")
    """

    def __init__(self, name: str):
        """
        Creates a new instance of the service.

        :param name: a service name.
        """
        super().__init__(name)
        self._dependency_resolver.put('service', 'none')
        self.__command_set: CommandSet = None

    def register(self):
        """
        Registers all actions in AWS Lambda function.
        """

        def wrapper(command):
            # wrapper for passing context
            def action(params):
                trace_id = None if params is None else params.get('trace_id')

                args = Parameters.from_value(params)
                if trace_id:
                    args.remove('trace_id')

                timing = self._instrument(trace_id, name)
                try:
                    return command.execute(trace_id, args)
                except Exception as e:
                    timing.end_failure(e)
                finally:
                    timing.end_timing()

            return action

        service: ICommandable = self._dependency_resolver.get_one_required('service')
        self.__command_set = service.get_command_set()

        commands = self.__command_set.get_commands()
        for index in range(len(commands)):
            command = commands[index]
            name = command.get_name()

            self._register_action(name, None, wrapper(command))

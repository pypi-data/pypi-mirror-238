# -*- coding: utf-8 -*-
from abc import ABC

from pip_services4_rpc.commands import CommandSet, ICommandable
from pip_services4_components.exec import Parameters
from pip_services4_components.context import Context
from .LambdaFunction import LambdaFunction


class CommandableLambdaFunction(LambdaFunction, ABC):
    """
    Abstract AWS Lambda function, that acts as a container to instantiate and run components
    and expose them via external entry point. All actions are automatically generated for commands
    defined in :class:`ICommandable <pip_services4_rpc.commands.ICommandable.ICommandable>` components. Each command is exposed as an action defined by "cmd" parameter.

    Container configuration for this Lambda function is stored in <code>"./config/config.yml"</code> file.
    But this path can be overriden by <code>CONFIG_PATH</code> environment variable.

    Note: This component has been deprecated. Use LambdaService instead.

    ### References ###
        - `*:logger:*:*:1.0`                   (optional) :class:`ContextInfo <pip_services3_components.log.ILogger.ILogger>` components to pass log messages
        - `*:counters:*:*:1.0`                 (optional) :class:`ContextInfo <pip_services3_components.count.ICounters.ICounters>` components to pass collected measurements
        - `*:service:lambda:*:1.0`              (optional) :class:`ILambdaController <pip_services4_aws.controllers.ILambdaService.ILambdaController>` controllers to handle action requests
        - `*:service:commandable-lambda:*:1.0`  (optional) :class:`ILambdaController <pip_services4_aws.controllers.ILambdaService.ILambdaController>` controllers to handle action requests

    See :class:`ILambdaService <pip_services4_aws.clients.LambdaClient.LambdaClient>`

    Example:

    .. code-block:: python

        class MyLambdaFunction(CommandableLambdaFunction):

            ...

            def __init__()

                super().__init__("mygroup", "MyGroup lambda function");
                self._dependency_resolver.put(
                    "service",
                    Descriptor("mygroup","service","*","*","1.0")
                )

                self.__service: IMyService = None


        lambda = MyLambdaFunction()

        service.run()
        print("MyLambdaFunction is started")
    """

    def __init__(self, name: str, description: str = None):
        """
        Creates a new instance of this lambda function.

        :param name: (optional) a container name (accessible via ContextInfo)
        :param description: (optional) a container description (accessible via ContextInfo)
        """
        super().__init__(name, description)
        self._dependency_resolver.put('controller', 'none')

    def __register_command_set(self, command_set: CommandSet):
        commands = command_set.get_commands()

        for index in range(len(commands)):
            command = commands[index]

            def wrapper(command):
                # wrapper for passing context
                def action(params: dict):
                    context = Context.from_trace_id(params.get('trace_id'))
                    args = Parameters.from_value(params)
                    timing = self._instrument(context, self._info.name + '.' + command.get_name())

                    try:
                        result = command.execute(context, args)
                        timing.end_timing()
                        return result
                    except Exception as e:
                        timing.end_timing(e)
                        raise e

                return action

            self._register_action(command.get_name(), None, wrapper(command))

    def register(self):
        """
        Registers all actions in this lambda function.
        """
        service: ICommandable = self._dependency_resolver.get_one_required('service')
        command_set = service.get_command_set()
        self.__register_command_set(command_set)

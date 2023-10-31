# -*- coding: utf-8 -*-
from typing import Optional, Any

from pip_services4_components.context import IContext
from pip_services4_aws.clients.CommandableLambdaClient import CommandableLambdaClient


class TestCommandableLambdaClient(CommandableLambdaClient):

    def __init__(self, base_route: str):
        super(TestCommandableLambdaClient, self).__init__(base_route)

    def call_command(self, cmd: str, context: Optional[IContext], params: dict) -> Any:
        """
        Calls a remote action in AWS Lambda function.
        The name of the action is added as "cmd" parameter
        to the action parameters.

        :param cmd: an action name
        :param context: (optional) transaction id to trace execution through call chain.
        :param params: command parameters.
        :return: action result.
        """
        return super(TestCommandableLambdaClient, self).call_command(cmd, context, params)

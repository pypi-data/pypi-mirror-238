# -*- coding: utf-8 -*-
from typing import Optional, Any

from pip_services4_components.context import IContext
from pip_services4_aws.clients.LambdaClient import LambdaClient


class TestLambdaClient(LambdaClient):
    def __init__(self):
        super(TestLambdaClient, self).__init__()

    def call(self, cmd: str, context: Optional[IContext], params: dict = None) -> Any:
        """
        Calls a AWS Lambda Function action.

        :param cmd: an action name to be called.
        :param context: (optional) transaction id to trace execution through call chain.
        :param params: (optional) action parameters.
        :return: action result.
        """
        return super()._call(cmd, context, params or {})

    def call_one_way(self, cmd: str, context: Optional[IContext], params: dict = None) -> Any:
        """
        Calls a AWS Lambda Function action asynchronously without waiting for response.

        :param cmd: an action name to be called.
        :param context: (optional) transaction id to trace execution through call chain.
        :param params: (optional) action parameters.
        :return: action result.
        """
        return super()._call_one_way(cmd, context, params)

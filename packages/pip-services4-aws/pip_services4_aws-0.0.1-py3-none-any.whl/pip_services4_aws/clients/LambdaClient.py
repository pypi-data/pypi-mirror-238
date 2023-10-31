# -*- coding: utf-8 -*-
import json
from abc import ABC
from copy import deepcopy
from typing import Any, Optional

from boto3 import client
from botocore.config import Config
from pip_services4_commons.convert import JsonConverter
from pip_services4_commons.errors import UnknownException, InvocationException
from pip_services4_components.config import IConfigurable, ConfigParams
from pip_services4_components.refer import IReferenceable, DependencyResolver, IReferences
from pip_services4_components.run import IOpenable
from pip_services4_components.context import IContext
from pip_services4_data.keys import IdGenerator
from pip_services4_observability.count import CompositeCounters
from pip_services4_observability.log import CompositeLogger
from pip_services4_observability.trace import CompositeTracer
from pip_services4_rpc.trace import InstrumentTiming

from pip_services4_aws.connect import AwsConnectionParams
from pip_services4_aws.connect import AwsConnectionResolver


class LambdaClient(IOpenable, IConfigurable, IReferenceable, ABC):
    """
    Abstract client that calls AWS Lambda Functions.

    When making calls "cmd" parameter determines which what action shall be called, while
    other parameters are passed to the action itself.

    ### Configuration parameters ###

        - connections:
            - discovery_key:               (optional) a key to retrieve the connection from :class:`IDiscovery <pip_services3_components.connect.IDiscovery.IDiscovery>`
            - region:                      (optional) AWS region
        - credentials:
            - store_key:                   (optional) a key to retrieve the credentials from :class:`ICredentialStore <pip_services3_components.auth.ICredentialStore.ICredentialStore>`
            - access_id:                   AWS access/client id
            - access_key:                  AWS access/client id
        - options:
            - connect_timeout:             (optional) connection timeout in milliseconds (default: 10 sec)

    ### References ###
        - `*:logger:*:*:1.0`           (optional) :class:`ILogger <pip_services3_components.log.ILogger.ILogger>` components to pass log messages
        - `*:counters:*:*:1.0`         (optional) :class:`ICounters <pip_services3_components.count.ICounters.ICounters>` components to pass collected measurements
        - `*:discovery:*:*:1.0`        (optional) :class:`IDiscovery <pip_services3_components.connect.IDiscovery.IDiscovery>` controllers to resolve connection
        - `*:credential-store:*:*:1.0`  (optional) Credential stores to resolve credentials

    See :class:`CommandableLambdaClient <pip_services4_aws.clients.CommandableLambdaClient.CommandableLambdaClient>`,
    :class:`LambdaFunction <pip_services4_aws.containers.LambdaFunction.LambdaFunction>`

    Example:

    .. code-block:: python

        class MyLambdaClient(LambdaClient, IMyClient):
            ...

            def get_data(self, context: Optional[IContext], id: str) -> MyData: 
                timing = self._instrument(context, 'myclient.get_data')
                result = self._call("get_data" ccontext, { 'id': id })
                timing.end_timing()
                return result
            
            ...
        

        client = MyLambdaClient()
        client.configure(ConfigParams.from_tuples(
            "connection.region", "us-east-1",
            "connection.access_id", "XXXXXXXXXXX",
            "connection.access_key", "XXXXXXXXXXX",
            "connection.arn", "YYYYYYYYYYYYY"
        ))

        result = client.get_data("123", "1")
    """

    def __init__(self):
        self.__connect_timeout: int = 10000

        # The reference to AWS Lambda Function.
        self._lambda: Any = None

        # The opened flag.
        self._opened: bool = False

        # The AWS connection parameters
        self._connection: AwsConnectionParams = None

        # The dependencies resolver.
        self._dependency_resolver: DependencyResolver = DependencyResolver()

        # The connection resolver.
        self._connection_resolver: AwsConnectionResolver = AwsConnectionResolver()

        # The logger.
        self._logger: CompositeLogger = CompositeLogger()

        # The performance counters.
        self._counters: CompositeCounters = CompositeCounters()

        # The tracer.
        self._tracer: CompositeTracer = CompositeTracer()

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self._connection_resolver.configure(config)
        self._dependency_resolver.configure(config)

        self.__connect_timeout = config.get_as_integer_with_default('options.connect_timeout', self.__connect_timeout)

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self._logger.set_references(references)
        self._counters.set_references(references)
        self._connection_resolver.set_references(references)
        self._dependency_resolver.set_references(references)

    def _instrument(self, context: Optional[IContext], name: str) -> InstrumentTiming:
        """
        Adds instrumentation to log calls and measure call time.
        It returns a CounterTiming object that is used to end the time measurement.

        :param context: (optional) transaction id to trace execution through call chain.
        :param name: a method name.
        :return: object to end the time measurement.
        """
        self._logger.trace(context, "Executing %s method", name)
        self._counters.increment_one(name + ".exec_count")

        counter_timing = self._counters.begin_timing(name + ".exec_time")
        trace_timing = self._tracer.begin_trace(context, name, None)
        return InstrumentTiming(context, name, "exec",
                                self._logger, self._counters, counter_timing, trace_timing)

    def is_open(self) -> bool:
        """
        Checks if the component is opened.

        :return: true if the component has been opened and false otherwise.
        """
        return self._opened

    def open(self, context: Optional[IContext]):
        """
        Opens the component.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if self.is_open():
            return

        self._connection = self._connection_resolver.resolve(context)

        config = Config(connect_timeout=round(self.__connect_timeout / 1000))
        self._lambda = client('lambda',  # 's3'
                              aws_access_key_id=self._connection.get_access_id(),
                              aws_secret_access_key=self._connection.get_access_key(),
                              region_name=self._connection.get_region(),
                              config=config)

        self._opened = True
        self._logger.debug(context, "Lambda client connected to %s", self._connection.get_arn())

    def close(self, context: Optional[IContext]):
        """
        Closes component and frees used resources.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        # Todo: close listening?
        if not self.is_open():
            return
        self._opened = False

    def _invoke(self, invocation_type: str, cmd: str, context: Optional[IContext], args: Any) -> Any:
        """
        Performs AWS Lambda Function invocation.

        :param invocation_type: an invocation type: "RequestResponse" or "Event"
        :param cmd: an action name to be called.
        :param context: (optional) transaction id to trace execution through call chain.
        :param args: action arguments
        :return: action result.
        """
        if cmd is None:
            raise UnknownException(None, 'NO_COMMAND', 'Missing Seneca pattern cmd')

        args = deepcopy(args)
        args['cmd'] = cmd
        args['trace_id'] = context or IdGenerator.next_short()

        params = {
            'FunctionName': self._connection.get_arn(),
            'InvocationType': invocation_type,
            'LogType': 'None',
            'Payload': args if isinstance(args, (bytes, bytearray)) else bytes(JsonConverter.to_json(args), 'utf-8')
        }

        try:
            data = self._lambda.invoke(**params)
            result = data['Payload'].read()

            if isinstance(result, (str, bytes, bytearray)):
                try:
                    result = json.loads(result)
                except Exception as e:
                    raise InvocationException(
                        context,
                        'DESERIALIZATION_FAILED',
                        'Failed to deserialize result'
                    ).with_cause(e)

            return result

        except Exception as e:
            raise InvocationException(
                context,
                'CALL_FAILED',
                'Failed to invoke lambda function'
            ).with_cause(e)

    def _call(self, cmd: str, context: Optional[IContext], params: dict = None) -> Any:
        """
        Calls a AWS Lambda Function action.

        :param cmd: an action name to be called.
        :param context: (optional) transaction id to trace execution through call chain.
        :param params: (optional) action parameters.
        :return: action result.
        """
        return self._invoke('RequestResponse', cmd, context, params or {})

    def _call_one_way(self, cmd: str, context: Optional[IContext], params: dict = None) -> Any:
        """
        Calls a AWS Lambda Function action asynchronously without waiting for response.

        :param cmd: an action name to be called.
        :param context: (optional) transaction id to trace execution through call chain.
        :param params: (optional) action parameters.
        :return: action result.
        """
        return self._invoke('Event', cmd, context, params or {})

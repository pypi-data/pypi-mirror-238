# -*- coding: utf-8 -*-
from typing import Optional, Any

from pip_services4_components.context import IContext

from .AzureFunctionClient import AzureFunctionClient


class CommandableAzureFunctionClient(AzureFunctionClient):
    """
    Abstract client that calls commandable Azure Functions.

    Commandable controllers are generated automatically for
    :class:`ICommandable <pip_services4_commons.commands.ICommandable.ICommandable>` objects.
    Each command is exposed as action determined by "cmd" parameter.

    ### Configuration parameters ###
        - connections:
            - uri:                         (optional) full connection string or use protocol, app_name and function_name to build
            - protocol:                    (optional) connection protocol
            - app_name:                    (optional) Azure Function application name
            - function_name:               (optional) Azure Function name
        - credentials:
            - auth_code:                   Azure Function auth code if use custom authorization provide empty string

    ### References ###
        - `*:logger:*:*:1.0`            (optional) :class:`ILogger <pip_services4_components.log.ILogger.ILogger>`  components to pass log messages
        - `*:counters:*:*:1.0`          (optional) :class:`ICounters <pip_services4_components.count.ICounters.ICounters>`  components to pass collected measurements
        - `*:discovery:*:*:1.0`        (optional) :class:`IDiscovery <pip_services4_components.connect.IDiscovery.IDiscovery>` controllers to resolve connection
        - `*:credential-store:*:*:1.0`   (optional) Credential stores to resolve credentials

    .. code-block:: python

        class MyCommandableAzureClient(CommandableAzureFunctionClient, IMyClient):
            ...

            def get_data(self, context: Optional[IContext], id: str) -> Any:
                return self.call_command('get_data', context, {'id': id})

            ...

        client = MyCommandableAzureClient('client_name')
        client.configure(ConfigParams.from_еuples(
            "connection.uri", "http://myapp.azurewebsites.net/api/myfunction",
            "connection.protocol", "http",
            "connection.app_name", "myapp",
            "connection.function_name", "myfunction"
            "credential.auth_code", "XXXX"
        ))

        result = client.get_data("123", "1")

    """

    def __init__(self, name: str):
        """
        Creates a new instance of this client.

        :param name: a service name.
        """
        super().__init__()
        self.__name = name

    def call_command(self, cmd: str, context: Optional[IContext], params: dict) -> Any:
        """
        Calls a remote action in Azure Function.
        The name of the action is added as "cmd" parameter
        to the action parameters.

        :param cmd: an action name
        :param context: (optional) transaction id to trace execution through call chain.
        :param params: command parameters.
        :return: action result.
        """
        timing = self._instrument(context, self.__name + '.' + cmd)
        try:
            result = self._call(cmd, context, params)
            timing.end_timing()
            return result
        except Exception as err:
            timing.end_failure(err)
            return err
        finally:
            timing.end_timing()

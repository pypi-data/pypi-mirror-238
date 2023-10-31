# -*- coding: utf-8 -*-
from typing import Any, Optional

from pip_services4_commons.data import StringValueMap
from pip_services4_commons.errors import ConfigException
from pip_services4_components.config import ConfigParams
from pip_services4_components.context import IContext, ContextResolver
from pip_services4_config.auth import CredentialParams
from pip_services4_config.connect import ConnectionParams


class AzureConnectionParams(ConfigParams):
    """
    Contains connection parameters to authenticate against Azure Functions
    and connect to specific Azure Function.

    The class is able to compose and parse Azure Function connection parameters.

    ### Configuration parameters ###

        - connections:
            - uri:           full connection uri with specific app and function name
            - protocol:      connection protocol
            - app_name:      alternative app name
            - function_name: application function name
        - credentials:
            - auth_code:     authorization code or null if using custom auth

    In addition to standard parameters :class:`CredentialParams <pip_services4_components.auth.CredentialParams.CredentialParams>` may contain any number of custom parameters

    See :class:`AzureConnectionResolver <pip_services4_azure.connect.AzureConnectionResolver.AzureConnectionResolver>`

    Example:

    .. code-block:: python
        connection = AzureConnectionParams.from_tuples(
            "connection.uri", "http://myapp.azurewebsites.net/api/myfunction",
            "connection.protocol", "http",
            "connection.app_name", "myapp",
            "connection.function_name", "myfunction",
            "connection.auth_code", "code",
        )

        uri = connection.get_function_uri()             # Result: "http://myapp.azurewebsites.net/api/myfunction"
        protocol = connection.get_protocol()            # Result: "http"
        appName = connection.get_app_name()             # Result: "myapp"
        functionName = connection.get_function_name()   # Result: "myfunction"
        authCode = connection.get_auth_code()           # Result: "code"
    """

    def __init__(self, values: Any = None):
        """
        Gets the Azure function connection protocol.

        :param values: the Azure function connection protocol.
        """
        super().__init__(values)

    def get_protocol(self) -> Optional[str]:
        """
        Gets the Azure function connection protocol.

        :return: the Azure function connection protocol.
        """
        return super().get_as_nullable_string('protocol')

    def set_protocol(self, value: str):
        """
        Sets the Azure function connection protocol.

        :param value: a new Azure function connection protocol.
        """
        super().put('protocol', value)

    def get_function_uri(self) -> str:
        """
        Gets the Azure function uri.

        :return: the Azure function uri.
        """
        return super().get_as_nullable_string('uri')

    def set_function_uri(self, value: str):
        """
        Sets the Azure function uri.

        :param value: a new Azure function uri.
        """
        super().put('uri', value)

    def get_app_name(self) -> Optional[str]:
        """
        Gets the Azure app name.

        :return: the Azure app name.
        """
        return super().get_as_nullable_string('app_name')

    def set_app_name(self, value: str):
        """
        Sets the Azure app name.

        :param value: a new Azure app name.
        """
        return super().put('app_name', value)

    def get_function_name(self) -> Optional[str]:
        """
        Gets the Azure function name.

        :return: the Azure function name.
        """
        return super().get_as_nullable_string('function_name')

    def set_function_name(self, value: str):
        """
        Sets the Azure function name.

        :param value: a new Azure function name.
        """
        super().put('function_name', value)

    def get_auth_code(self) -> Optional[str]:
        """
        Gets the Azure auth code.

        :return: the Azure auth code.
        """
        return super().get_as_nullable_string('auth_code')

    def set_auth_code(self, value: str):
        """
        Sets the Azure auth code.

        :param value: a new Azure auth code.
        """
        super().put('auth_code', value)

    @staticmethod
    def from_string(line: str) -> 'AzureConnectionParams':
        """
        Creates a new AzureConnectionParams object filled with key-value pairs serialized as a string.

        :param line: a string with serialized key-value pairs as "key1=value1;key2=value2;..."
                     Example: "Key1=123;Key2=ABC;Key3=2016-09-16T00:00:00.00Z"
        :return: a new AzureConnectionParams object.
        """
        map_values = StringValueMap.from_string(line)
        return AzureConnectionParams(map_values)

    def validate(self, context: Optional[IContext]):
        """
        Validates this connection parameters

        :param context: (optional) transaction id to trace execution through call chain.
        """
        uri = self.get_function_uri()
        protocol = self.get_protocol()
        app_name = self.get_app_name()
        function_name = self.get_function_name()

        if not uri and not (app_name and function_name and protocol):
            raise ConfigException(
                ContextResolver.get_trace_id(context),
                "NO_CONNECTION_URI",
                "No uri, app_name and function_name is configured in Azure function uri"
            )

        if protocol and 'http' != protocol and 'https' != protocol:
            raise ConfigException(
                ContextResolver.get_trace_id(context),
                "WRONG_PROTOCOL", "Protocol is not supported by REST connection"
            ).with_details("protocol", protocol)

        # if self.get_auth_code() is None:
        #     raise ConfigException(
        #         context,
        #         "NO_ACCESS_KEY",
        #         "No access_key is configured in Azure credential"
        #     )

    @staticmethod
    def from_config(config: ConfigParams) -> 'AzureConnectionParams':
        """
        Retrieves AzureConnectionParams from configuration parameters.
        The values are retrieves from "connection" and "credential" sections.

        :param config: configuration parameters
        :return: the generated AzureConnectionParams object.
        """
        result = AzureConnectionParams()

        credentials = CredentialParams.many_from_config(config)
        for credential in credentials:
            result.append(credential)

        connections = ConnectionParams.many_from_config(config)
        for connection in connections:
            result.append(connection)

        return result

    @staticmethod
    def merge_configs(*configs: 'ConfigParams') -> 'AzureConnectionParams':
        """
        Retrieves AzureConnectionParams from multiple configuration parameters.
        The values are retrieves from "connection" and "credential" sections.

        :param configs: a list with configuration parameters
        :return: the generated AzureConnectionParams object.
        """
        config = ConfigParams.merge_configs(*configs)
        return AzureConnectionParams(config)

    @staticmethod
    def from_tuples(*tuples: Any) -> 'AzureConnectionParams':
        """
        Creates a new ConfigParams object filled with provided key-args pairs called tuples.
        Tuples parameters contain a sequence of key1, value1, key2, value2, ... pairs.

        :param tuples: the tuples to fill a new ConfigParams object.

        :return: a new ConfigParams object.
        """
        config_params = super(AzureConnectionParams, AzureConnectionParams).from_tuples(*tuples)
        return AzureConnectionParams.from_config(config_params)

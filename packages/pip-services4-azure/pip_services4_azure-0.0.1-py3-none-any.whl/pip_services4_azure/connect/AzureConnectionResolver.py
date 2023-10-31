# -*- coding: utf-8 -*-
from typing import Optional

from pip_services4_components.config import IConfigurable, ConfigParams
from pip_services4_components.refer import IReferenceable, IReferences
from pip_services4_config.auth import CredentialResolver
from pip_services4_config.connect import ConnectionResolver
from urllib3.util.url import parse_url, Url

from pip_services4_components.context import IContext

from .AzureConnectionParams import AzureConnectionParams


class AzureConnectionResolver(IConfigurable, IReferenceable):
    """
    Helper class to retrieve Azure connection and credential parameters,
    validate them and compose a AzureConnectionParams value.

    ### Configuration parameters ###
        - connections:
            - uri:           full connection uri with specific app and function name
            - protocol:      connection protocol
            - app_name:      alternative app name
            - function_name: application function name
        - credentials:
            - auth_code:     authorization code or null if using custom auth

    ### References ###
        - *:credential-store:*:*:1.0   (optional) Credential stores to resolve credentials

    See :class:`ConnectionParams <pip_services4_components.connect.ConnectionParams.ConnectionParams>` (in the Pip.Services components package),
    :class:`IDiscovery <pip_services4_components.connect.IDiscovery.IDiscovery>` (in the Pip.Services components package)

    .. code-block:: python

        config = ConfigParams.from_tuples(
            "connection.uri", "http://myapp.azurewebsites.net/api/myfunction",
            "connection.app_name", "myapp",
            "connection.function_name", "myfunction",
            "credential.auth_code", "XXXXXXXXXX",
        )

        connection_resolver = AzureConnectionResolver()
        connection_resolver.configure(config)
        connection_resolver.set_references(references)

        connection_params = connection_resolver.resolve("123")
    """

    def __init__(self):
        self._connection_resolver: ConnectionResolver = ConnectionResolver()
        self._credential_resolver: CredentialResolver = CredentialResolver()

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self._connection_resolver.configure(config)
        self._credential_resolver.configure(config)

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self._connection_resolver.set_references(references)
        self._credential_resolver.set_references(references)

    def resolve(self, context: Optional[IContext], ) -> AzureConnectionParams:
        """
        Resolves connection and credential parameters and generates a single
        AzureConnectionParams value.

        :param context: (optional) transaction id to trace execution through call chain.
        :return: receives AzureConnectionParams value or raise error.
        """
        connection = AzureConnectionParams()

        connection_params = self._connection_resolver.resolve(context)
        connection.append(connection_params)

        credential_params = self._credential_resolver.lookup(context)
        connection.append(credential_params)

        # Perform validation
        connection.validate(context)

        connection = self.__compose_connection(connection)

        return connection

    def __compose_connection(self, connection: AzureConnectionParams) -> AzureConnectionParams:
        connection = AzureConnectionParams.merge_configs(connection)

        uri = connection.get_function_uri()

        if uri is None or uri == '':
            protocol = connection.get_protocol()
            app_name = connection.get_app_name()
            function_name = connection.get_function_name()
            # http://myapp.azurewebsites.net/api/myfunction
            uri = f'{protocol}://{app_name}.azurewebsites.net/api/{function_name}'

            connection.set_function_uri(uri)
        else:
            address: Url = parse_url(uri)
            protocol = address.scheme
            app_name = address.host.replace('.azurewebsites.net', '')
            function_name = address.path.replace('/api/', '')

            connection.set_protocol(protocol)
            connection.set_app_name(app_name)
            connection.set_function_name(function_name)

        return connection
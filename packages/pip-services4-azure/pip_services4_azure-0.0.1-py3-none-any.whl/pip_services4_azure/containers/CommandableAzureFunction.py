# -*- coding: utf-8 -*-
import json
from typing import Optional, Any

import azure.functions as func
from pip_services4_commons.convert import JsonConverter
from pip_services4_components.context import Context

from pip_services4_components.exec import Parameters
from pip_services4_data.query import DataPage
from pip_services4_rpc.commands import CommandSet, ICommand, ICommandable
from pip_services4_rpc.trace import InstrumentTiming

from .AzureFunction import AzureFunction
from .AzureFunctionContextHelper import AzureFunctionContextHelper


class CommandableAzureFunction(AzureFunction):
    """
    Abstract Azure Function function, that acts as a container to instantiate and run components
    and expose them via external entry point. All actions are automatically generated for commands
    defined in :class:`ICommandable <pip_services4_commons.commands.ICommandable.ICommandable>`. Each command is exposed as an action defined by "cmd" parameter.
    
    Container configuration for this Azure Function is stored in `"./config/config.yml"` file.
    But this path can be overridden by `CONFIG_PATH` environment variable.
    
    Note: This component has been deprecated. Use Azure FunctionService instead.
    
    ### References ###
        - `*:logger:*:*:1.0`:            (optional) :class:`ILogger <pip_services4_components.log.ILogger.ILogger>`  components to pass log messages
        - `*:counters:*:*:1.0`:          (optional) :class:`ICounters <pip_services4_components.count.ICounters.ICounters>`  components to pass collected measurements
        - `*:service:azurefunc:*:1.0`: (optional) :class:`IAzureFunctionController <pip_services4_azure.controllers.IAzureFunctionController.IAzureFunctionController>` controllers to handle action requests
        - `*:service:commandable-azurefunc:*:1.0`: (optional) :class:`IAzureFunctionController <pip_services4_azure.controllers.IAzureFunctionController.IAzureFunctionController>` controllers to handle action requests

    Example:

    .. code-block:: python
        class MyAzureFunctionFunction(CommandableAzureFunction):
            def __init__(self):
                super().__init__("mygroup", "MyGroup AzureFunction")
                self._dependency_resolver.put("controller", Descriptor("mygroup", "service", "*", "*", "1.0"))
                
        azure_function = MyAzureFunctionFunction()
        service.run()
        print("MyAzureFunction is started")
    """

    def __init__(self, name: Optional[str], description: Optional[str]):
        """
        Creates a new instance of this Azure Function.

        :param name: (optional) a container name (accessible via ContextInfo)
        :param description: (optional) a container description (accessible via ContextInfo)
        """
        super().__init__(name, description)
        self._dependency_resolver.put('service', 'none')

    def _get_parameters(self, context: func.HttpRequest) -> Parameters:
        """
        Returns body from Azure Function context.
        This method can be overloaded in child classes

        :param context: Azure Function context
        :return: Returns Parameters from context
        """
        return AzureFunctionContextHelper.get_parameters(context)

    def __register_command_set(self, command_set: CommandSet):
        commands = command_set.get_commands()
        for i in range(len(commands)):
            command = commands[i]

            def wrapper(command: ICommand):
                # wrapper for passing context
                def action(context: func.HttpRequest):
                    ctx = Context.from_trace_id(self._get_trace_id(context))
                    args = self._get_parameters(context)
                    timing: InstrumentTiming = self._instrument(ctx,
                                                                self._info.name + '.' + command.get_name())

                    try:
                        result = command.execute(ctx, args)
                        # Conversion to response data format
                        result = self.__to_response_format(result)
                        return result
                    except Exception as e:
                        timing.end_failure(e)
                        return func.HttpResponse(
                            body=JsonConverter.to_json(e),
                            status_code=400
                        )
                    finally:
                        timing.end_timing()

                return action

            self._register_action(command.get_name(), None, wrapper(command))

    def register(self):
        """
        Registers all actions in this Azure Function.
        """
        service: ICommandable = self._dependency_resolver.get_one_required('service')
        command_set = service.get_command_set()
        self.__register_command_set(command_set)

    def __to_response_format(self, res: Any) -> func.HttpResponse:
        if res is None:
            return func.HttpResponse(status_code=204)
        if not isinstance(res, (str, bytes, func.HttpResponse)):
            if hasattr(res, 'to_dict'):
                res = res.to_dict()
            elif hasattr(res, 'to_json'):
                if isinstance(res, DataPage) and len(res.data) > 0 and not isinstance(res.data[0], dict):
                    res.data = json.loads(JsonConverter.to_json(res.data))
                res = res.to_json()
            else:
                res = JsonConverter.to_json(res)

        return func.HttpResponse(body=json.dumps(res))
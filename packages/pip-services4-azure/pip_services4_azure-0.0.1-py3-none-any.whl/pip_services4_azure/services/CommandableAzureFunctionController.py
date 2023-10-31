# -*- coding: utf-8 -*-
import json
from typing import Any

import azure.functions as func
from pip_services4_commons.convert import JsonConverter

from pip_services4_components.context import Context
from pip_services4_components.exec import Parameters
from pip_services4_data.query import DataPage
from pip_services4_rpc.commands import CommandSet, ICommandable, ICommand

from .AzureFunctionController import AzureFunctionController
from ..containers.AzureFunctionContextHelper import AzureFunctionContextHelper


class CommandableAzureFunctionController(AzureFunctionController):
    """
    Abstract service that receives commands via Azure Function protocol
    to operations automatically generated for commands defined in :class:`ICommandable <pip_services4_commons.commands.ICommandable.ICommandable>` components.
    Each command is exposed as invoke method that receives command name and parameters.

    Commandable controllers require only 3 lines of code to implement a robust external
    Azure Function-based remote interface.

    This service is intended to work inside Azure Function container that
    exploses registered actions externally.

    ### Configuration parameters ###
        - dependencies:
            - controller:            override for Controller dependency

    ### References ###
        - `*:logger:*:*:1.0`            (optional) :class:`ILogger <pip_services4_components.log.ILogger.ILogger>`  components to pass log messages
        - `*:counters:*:*:1.0`          (optional) :class:`ICounters <pip_services4_components.count.ICounters.ICounters>`  components to pass collected measurements

    See: :class:`AzureFunctionController <pip_services4_azure.controllers.AzureFunctionController.AzureFunctionController>`

    Example:

    .. code-block:: python
        class MyCommandableAzureFunctionService(CommandableAzureFunctionController):
            def __init__(self):
                super(MyCommandableAzureFunctionService, self).__init__()
                self._dependency_resolver.put(
                    "controller", Descriptor("mygroup", "service", "*", "*", "1.0")
                )


        controller = MyCommandableAzureFunctionService()
        controller.set_references(References.fromTuples(
            Descriptor("mygroup", "service", "default", "default", "1.0"), controller
        ))

        controller.open("123")
        print("The Azure Function controller is running")

    """

    def __init__(self, name: str):
        """
        Creates a new instance of the service.

        :param name: a service name.
        """
        super(CommandableAzureFunctionController, self).__init__(name)
        self._dependency_resolver.put('service', 'none')

        self._command_set: CommandSet = None

    def _get_parameters(self, context: func.HttpRequest) -> Parameters:
        """
        Returns body from Azure Function context.
        This method can be overloaded in child classes

        :param context: Azure Function context
        :return: Returns Parameters from context
        """
        return AzureFunctionContextHelper.get_parameters(context)

    def register(self):
        """
        Registers all actions in Azure Function.
        """
        service: ICommandable = self._dependency_resolver.get_one_required('service')
        self._command_set = service.get_command_set()

        commands = self._command_set.get_commands()
        for index in range(len(commands)):
            command = commands[index]
            name = command.get_name()

            def wrapper(command: ICommand):
                # wrapper for passing context
                def action(context: func.HttpRequest):
                    ctx = Context.from_trace_id(self._get_tace_id(context))
                    args = self._get_parameters(context)
                    if 'trace_id' in args.keys():
                        args.remove('trace_id')

                    timing = self._instrument(ctx, command.get_name())
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

            self._register_action(name, None, wrapper(command))

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

# -*- coding: utf-8 -*-
import json
from abc import abstractmethod
from typing import Optional, List, Any, Callable

import azure.functions as func
from pip_services4_commons.errors import BadRequestException
from pip_services4_components.config import IConfigurable, ConfigParams

from pip_services4_components.context import IContext
from pip_services4_components.refer import IReferenceable, DependencyResolver, IReferences
from pip_services4_components.run import IOpenable
from pip_services4_data.validate import Schema
from pip_services4_observability.count import CompositeCounters
from pip_services4_observability.log import CompositeLogger
from pip_services4_observability.trace import CompositeTracer
from pip_services4_rpc.trace import InstrumentTiming

from .AzureFunctionAction import AzureFunctionAction
from .IAzureFunctionController import IAzureFunctionController
from ..containers.AzureFunctionContextHelper import AzureFunctionContextHelper


class AzureFunctionController(IAzureFunctionController, IOpenable, IConfigurable, IReferenceable):
    """
    Abstract service that receives remove calls via Azure Function protocol.

    This service is intended to work inside AzureFunction container that
    exposes registered actions externally.

    ### Configuration parameters ###
        - dependencies:
            - controller:            override for Controller dependency

    ### References ###
        - `*:logger:*:*:1.0`            (optional) :class:`ILogger <pip_services4_components.log.ILogger.ILogger>`  components to pass log messages
        - `*:counters:*:*:1.0`          (optional) :class:`ICounters <pip_services4_components.count.ICounters.ICounters>`  components to pass collected measurements

    Example:

    .. code-block:: python

        class MyAzureFunctionService(AzureFunctionController):
            def __init__(self):
                super().__init__('v1.myservice')
                self._dependency_resolver.put(
                    "service",
                    Descriptor("mygroup", "service", "*", "*", "1.0")
                )
                self.__service: IMyService = None

            def set_references(self, references: IReferences):
                super().set_references(references)
                self.__service = self._dependency_resolver.get_required("service")

            def __get_mydata(self, context: HttpRequest):
                data = context.get_json()
                trace_id = data.get('trace_id')
                id = data.get('id')
                return self.__service.get_my_data(trace_id, id)

            def register(self):
                self._register_action(
                    'get_mydata',
                    None,
                    self.__get_mydata
                )
                ...

        service = MyAzureFunctionService()
        service.configure(ConfigParams.from_tuples(
            "connection.protocol", "http",
            "connection.host", "localhost",
            "connection.port", 8080
        ))
        service.set_references(References.fromTuples(
            Descriptor("mygroup", "service", "default", "default", "1.0"), service
        ))
        service.open(Context.from_trace_id("123"))

    """

    def __init__(self, name: Optional[str]):
        """
        Creates an instance of this service.

        :param name: a service name to generate action cmd.
        """
        self.__name = name

        self.__actions: List[AzureFunctionAction] = []
        self.__interceptors: list = []
        self.__opened: bool = False

        # The dependency resolver.
        self._dependency_resolver: DependencyResolver = DependencyResolver()

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
        self._dependency_resolver.configure(config)

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self._logger.set_references(references)
        self._counters.set_references(references)
        self._tracer.set_references(references)
        self._dependency_resolver.set_references(references)

    def get_actions(self) -> List[AzureFunctionAction]:
        """
        Get all actions supported by the service.

        :return: an array with supported actions.
        """
        return self.__actions

    def _instrument(self, context: Optional[IContext], name: str) -> InstrumentTiming:
        """
        Adds instrumentation to log calls and measure call time.
        It returns a Timing object that is used to end the time measurement.

        :param context: (optional) transaction id to trace execution through call chain.
        :param name: a method name.
        :return: Timing object to end the time measurement.
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
        return self.__opened

    def open(self, context: Optional[IContext]):
        """
        Opens the component.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if self.__opened:
            return

        self.register()

        self.__opened = True

    def close(self, context: Optional[IContext]):
        """
        Closes component and frees used resources.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if not self.__opened:
            return

        self.__opened = False
        self.__actions = []
        self.__interceptors = []

    def _apply_validation(self, schema: Schema, action: Callable[[func.HttpRequest], func.HttpResponse]) -> Callable[
        [func.HttpRequest], func.HttpResponse]:
        # Create an action function
        def action_wrapper(context: func.HttpRequest) -> func.HttpResponse:
            # Validate object
            if schema and context:
                # Perform validation
                params = {'body': {} if not context.get_body() else context.get_json()}
                params.update(context.route_params)
                params.update(context.params)

                trace_id = self._get_tace_id(context)
                err = schema.validate_and_return_exception(trace_id, params, False)
                if err is not None:
                    return func.HttpResponse(
                        body=json.dumps(err.to_json()),
                        status_code=err.status
                    )

            result = action(context)
            return result

        return action_wrapper

    def _apply_interceptors(self, action: Callable[[func.HttpRequest], Any]) -> Callable[[func.HttpRequest], Any]:
        action_wrapper = action

        index = len(self.__interceptors) - 1
        while index >= 0:
            interceptor = self.__interceptors[index]
            action_wrapper = lambda _action: lambda params: interceptor(params, _action)(action_wrapper)

            index -= 1

        return action_wrapper

    def _generate_action_cmd(self, name: str) -> str:
        cmd = name
        if self.__name:
            cmd = self.__name + '.' + cmd
        return cmd

    def _register_action(self, name: str, schema: Schema, action: Callable[[func.HttpRequest], func.HttpResponse]):
        """
        Registers a action in Azure Function function.

        :param name: an action name
        :param schema: a validation schema to validate received parameters.
        :param action: an action function that is called when operation is invoked.
        """
        action_wrapper = self._apply_validation(schema, action)
        action_wrapper = self._apply_interceptors(action_wrapper)

        register_action: AzureFunctionAction = AzureFunctionAction(self._generate_action_cmd(name), schema,
                                                                   lambda params: action_wrapper(params))

        self.__actions.append(register_action)

    def _register_action_with_auth(self, name: str, schema: Schema,
                                   authorize: Callable[[func.HttpRequest, Callable[[func.HttpRequest], Any]], Any],
                                   action: Callable[[func.HttpRequest], func.HttpResponse]):
        """
        Registers an action with authorization.

        :param name: an action name
        :param schema: a validation schema to validate received parameters.
        :param authorize: an authorization interceptor
        :param action: an action function that is called when operation is invoked.
        """
        action_wrapper = self._apply_validation(schema, action)

        # Add authorization just before validation
        action_wrapper = lambda call: authorize(call, action_wrapper)

        action_wrapper = self._apply_interceptors(action_wrapper)

        register_action: AzureFunctionAction = AzureFunctionAction(self._generate_action_cmd(name), schema,
                                                                   lambda params: action_wrapper(params))

        self.__actions.append(register_action)

    def _register_interceptor(self, action: Callable[[func.HttpRequest, Callable[[func.HttpRequest], Any]], Any]):
        """
        Registers a middleware for actions in AWS Lambda service.

        :param action: an action function that is called when middleware is invoked.
        """
        self.__interceptors.append(action)

    @abstractmethod
    def register(self):
        """
        Registers all service routes in HTTP endpoint.

        This method is called by the service and must be overridden
        in child classes.
        """

    def _get_tace_id(self, context: func.HttpRequest) -> str:
        """
        Returns trace id from Azure Function context.
        This method can be overloaded in child classes

        :param context: the context context
        :return: returns trace id from context
        """
        return AzureFunctionContextHelper.get_trace_id(context)

    def _get_command(self, context: func.HttpRequest) -> str:
        """
        Returns command from Azure Function context.
        This method can be overloaded in child classes

        :param context: the context context
        :return: returns command from context
        """
        return AzureFunctionContextHelper.get_command(context)

    def act(self, context: func.HttpRequest) -> func.HttpResponse:
        """
        Calls registered action in this Azure Function.
        "cmd" parameter in the action parameters determine
        what action shall be called.

        This method shall only be used in testing.

        :param context: the context context.
        """
        cmd = self._get_command(context)
        trace_id = self._get_tace_id(context)

        if not cmd:
            raise BadRequestException(
                trace_id,
                'NO_COMMAND',
                'Cmd parameter is missing'
            )

        filtered = list(filter(lambda a: a.cmd == cmd, self.__actions))
        action: AzureFunctionAction = None if len(filtered) == 0 else filtered[0]
        if not action:
            raise BadRequestException(
                trace_id,
                'NO_ACTION',
                'Action ' + cmd + ' was not found'
            ).with_details('command', cmd)

        return action.action(context)

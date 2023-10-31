# -*- coding: utf-8 -*-
import azure.functions as func

from pip_services4_components.exec import Parameters


class AzureFunctionContextHelper:

    @staticmethod
    def get_trace_id(context: func.HttpRequest) -> str:
        """
        Returns trace id from Azure Function context.

        :param context: the Azure Function context
        :return: returns trace id from context
        """
        trace_id = '' if not context.get_body() else context.get_json().get('trace_id')
        try:
            if (trace_id is None or trace_id == '') and context.get_body():
                trace_id = context.get_json().get('trace_id', '')
                if trace_id is None or trace_id == '':
                    trace_id = context.params.get('trace_id', '')
        except Exception as e:
            # Ignore the error
            pass
        return trace_id

    @staticmethod
    def get_command(context: func.HttpRequest) -> str:
        """
        Returns command from Azure Function context.

        :param context: the Azure Function context
        :return: returns command from context
        """
        cmd = '' if not context.get_body() else context.get_json().get('cmd')
        try:
            if (cmd is None or cmd == '') and context.get_body():
                cmd = context.get_json().get('cmd')
                if cmd is None or cmd == '':
                    cmd = context.params.get('cmd')
        except Exception as e:
            # Ignore the error
            pass

        return cmd

    @staticmethod
    def get_parameters(context: func.HttpRequest) -> Parameters:
        """
        Returns body from Azure Function context http request.

        :param context: the Azure Function context
        :return: returns body from context
        """
        body = context.get_body() or None
        try:
            if body:
                body = context.get_json()
        except Exception as e:
            # Ignore the error
            pass

        return Parameters.from_value(body)

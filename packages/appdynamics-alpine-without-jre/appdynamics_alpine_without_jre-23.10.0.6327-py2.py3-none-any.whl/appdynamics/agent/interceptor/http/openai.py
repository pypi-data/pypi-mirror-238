# Copyright (c) AppDynamics, Inc., and its affiliates
# 2015
# All Rights Reserved

"""Intercept boto to ensure that HTTPS is reported correctly.

"""

from __future__ import unicode_literals
from . import HTTPConnectionInterceptor
import appdynamics.agent.interceptor.utils.openai_utils as openai_utils


class OpenAiMethodInstrumentor(HTTPConnectionInterceptor):
    def __init__(self, agent, cls):
        self.tier_model_metrics_mapping = dict()
        self.app_model_metrics_mapping = dict()
        self.tier_all_models_metrics_mapping = openai_utils._initialize_metrics(
            metric_prefix_path=openai_utils.TIER_METRIC_PATH,
            metric_suffix=openai_utils.METRIC_NAME_SEGREGATOR + openai_utils.ALL_MODELS_STRING,
            metric_dict=openai_utils.METRICS_DICT,
        )
        self.application_all_models_metrics_mapping = openai_utils._initialize_metrics(
            metric_prefix_path=openai_utils.APPLICATION_METRIC_PATH,
            metric_prefix=openai_utils.OPENAI_PREFIX,
            metric_suffix=openai_utils.METRIC_NAME_SEGREGATOR + openai_utils.ALL_MODELS_STRING,
            metric_dict=openai_utils.METRICS_DICT,
        )
        super(OpenAiMethodInstrumentor, self).__init__(agent, cls)

    def _create_model_metrics(self, model_name):
        if model_name not in self.tier_model_metrics_mapping:
            self.tier_model_metrics_mapping[model_name] = openai_utils._initialize_metrics(
                metric_prefix_path=openai_utils.TIER_METRIC_PATH + openai_utils.METRIC_PATH_SEGREGATOR + model_name,
                metric_dict=openai_utils.METRICS_DICT
            )
        if model_name not in self.app_model_metrics_mapping:
            self.app_model_metrics_mapping[model_name] = openai_utils._initialize_metrics(
                metric_prefix_path=openai_utils.APPLICATION_METRIC_PATH,
                metric_prefix=openai_utils.OPENAI_PREFIX,
                metric_suffix=openai_utils.METRIC_NAME_SEGREGATOR + model_name,
                metric_dict=openai_utils.METRICS_DICT
            )

    def _do_report_all_metrics(self, model_name, reporting_values):
        # Reporting indiviual model level performance metrics
        for metrics in (self.tier_model_metrics_mapping, self.app_model_metrics_mapping):
            openai_utils._report_metrics(
                metrics_dict=metrics[model_name],
                reporting_values=reporting_values,
                agent=self.agent
            )
        # Reporting indiviual model level performance metrics
        for metrics in (self.tier_all_models_metrics_mapping, self.application_all_models_metrics_mapping):
            openai_utils._report_metrics(
                metrics_dict=metrics,
                reporting_values=reporting_values,
                agent=self.agent
            )

    def make_exit_call(self):
        exit_call = None
        with self.log_exceptions():
            bt = self.bt
            if bt:
                host, port, scheme, url = openai_utils._get_backend_details()
                backend = self.get_backend(
                    host=host,
                    port=port,
                    scheme=scheme,
                    url=url
                )
                if backend:
                    exit_call = self.start_exit_call(bt, backend)
        self.end_exit_call(exit_call=exit_call)

    async def _acreate(self, acreate, *args, **kwargs):
        reporting_values = dict()
        acreate_respone = dict()
        reporting_values[openai_utils.CALLS_METRIC_NAME] = 1
        model = kwargs.get('model') or kwargs.get('engine')
        # creating model specfic metrics
        self._create_model_metrics(model_name=model)

        try:
            acreate_respone = await acreate(*args, **kwargs)
        except:
            reporting_values[openai_utils.ERROR_METRIC_NAME] = 1
            raise
        finally:
            self.make_exit_call()
            # Checking if exception was raised earlier or not
            if openai_utils.ERROR_METRIC_NAME not in reporting_values:
                try:
                    reporting_values.update(openai_utils._get_reporting_values_per_request(
                        model_name=model,
                        agent=self.agent,
                        endpoint_response=acreate_respone
                    ))
                except:
                    return acreate_respone

            # Reporting all metrics
            self._do_report_all_metrics(
                model_name=model,
                reporting_values=reporting_values,
            )
            reporting_values.clear()
        # returning response
        return acreate_respone

    def _create(self, create, *args, **kwargs):
        reporting_values = dict()
        create_respone = dict()
        reporting_values[openai_utils.CALLS_METRIC_NAME] = 1
        model = kwargs.get('model') or kwargs.get('engine')
        # creating model specfic metrics
        self._create_model_metrics(model_name=model)
        try:
            create_respone = create(*args, **kwargs)
        except:
            reporting_values[openai_utils.ERROR_METRIC_NAME] = 1
            raise
        finally:
            self.make_exit_call()
            # Checking if exception was raised earlier or not
            if openai_utils.ERROR_METRIC_NAME not in reporting_values:
                try:
                    reporting_values.update(openai_utils._get_reporting_values_per_request(
                        model_name=model,
                        agent=self.agent,
                        endpoint_response=create_respone
                    ))
                except:
                    return create_respone

            # Reporting all metrics
            self._do_report_all_metrics(
                model_name=model,
                reporting_values=reporting_values,
            )
            reporting_values.clear()
        # returning response
        return create_respone


def intercept_openai(agent, mod):
    for method_name in ['create', 'acreate']:
        OpenAiMethodInstrumentor(agent, mod.Completion).attach(method_name)
        OpenAiMethodInstrumentor(agent, mod.ChatCompletion).attach(method_name)

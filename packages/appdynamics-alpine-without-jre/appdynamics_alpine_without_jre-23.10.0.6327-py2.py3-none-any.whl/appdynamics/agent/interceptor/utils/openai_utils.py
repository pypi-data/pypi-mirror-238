import appdynamics.agent.models.custom_metrics as custom_metrics_mod
from appdynamics.lang import items, urlparse


COST_METRIC_NAME = "Cost"
TOKENS_METRIC_NAME = "Tokens"
CALLS_METRIC_NAME = "Calls per minute"
ERROR_METRIC_NAME = "Errors per minute"
ALL_MODELS_STRING = "All Models"
OPENAI = "OpenAI"
METRIC_NAME_SEGREGATOR = " - "
OPENAI_PREFIX = OPENAI + METRIC_NAME_SEGREGATOR
TIER_METRIC_PATH = "Agent|OpenAI"
APPLICATION_METRIC_PATH = "BTM|Application Summary"
RESPONSE_PROMPT_STRING = "prompt_tokens"
RESPONSE_COMPLETION_STRING = "completion_tokens"
RESPONSE_TOTAL_TOKEN_STRING = "total_tokens"
TIME_ROLLUP_STRING = "time_rollup_type"
CLUSTER_ROLLUP_STRING = "cluster_rollup_type"
HOLE_HANDLING_STRING = "hole_handling_type"
METRIC_PATH_SEGREGATOR = "|"
DEFAULT_OPENAI_ENDPOINT = "https://api.openai.com/v1"
METRICS_DICT = {
    COST_METRIC_NAME: {
        TIME_ROLLUP_STRING: custom_metrics_mod.TIME_SUM,
        CLUSTER_ROLLUP_STRING: None,
        HOLE_HANDLING_STRING: custom_metrics_mod.REGULAR_COUNTER
    },
    CALLS_METRIC_NAME: {
        TIME_ROLLUP_STRING: custom_metrics_mod.TIME_AVERAGE,
        CLUSTER_ROLLUP_STRING: None,
        HOLE_HANDLING_STRING: custom_metrics_mod.RATE_COUNTER
    },
    ERROR_METRIC_NAME: {
        TIME_ROLLUP_STRING: custom_metrics_mod.TIME_AVERAGE,
        CLUSTER_ROLLUP_STRING: None,
        HOLE_HANDLING_STRING: custom_metrics_mod.RATE_COUNTER
    },
    TOKENS_METRIC_NAME: {
        TIME_ROLLUP_STRING: custom_metrics_mod.TIME_SUM,
        CLUSTER_ROLLUP_STRING: None,
        HOLE_HANDLING_STRING: custom_metrics_mod.REGULAR_COUNTER
    },
}

MODEL_COST_MAP = {
    "babbage": {'prompt_cost': 5, 'completion_cost': 5},
    "curie": {'prompt_cost': 20, 'completion_cost': 20},
    "davinci": {'prompt_cost': 200, 'completion_cost': 200},
    "text-ada-001": {'prompt_cost': 4, 'completion_cost': 4},
    "text-babbage-001": {'prompt_cost': 5, 'completion_cost': 5},
    "text-curie-001": {'prompt_cost': 20, 'completion_cost': 20},
    "gpt-3.5-turbo": {'prompt_cost': 15, 'completion_cost': 20},
    "gpt-3.5-turbo-0613": {'prompt_cost': 30, 'completion_cost': 40},
    "gpt-3.5-turbo-16k": {'prompt_cost': 30, 'completion_cost': 40},
    "gpt-3.5-turbo-16k-0613": {'prompt_cost': 30, 'completion_cost': 40},
    "text-davinci-001": {'prompt_cost': 200, 'completion_cost': 200},
    "text-davinci-002": {'prompt_cost': 200, 'completion_cost': 200},
    "text-davinci-003": {'prompt_cost': 200, 'completion_cost': 200},
    "code-davinci-002": {'prompt_cost': 0, 'completion_cost': 0},
    "gpt-4": {'prompt_cost': 300, 'completion_cost': 600},
    "gpt-4-0613": {'prompt_cost': 300, 'completion_cost': 600},
    "gpt-4-32k": {'prompt_cost': 600, 'completion_cost': 1200},
    "gpt-4-32k-0613": {'prompt_cost': 600, 'completion_cost': 1200},

    # cisco chat-ai
    "gpt-35-turbo": {'prompt_cost': 15, 'completion_cost': 20},
}


def get_tokens_per_request(method_response, token_type=RESPONSE_PROMPT_STRING):
    try:
        return method_response['usage'][token_type]
    except Exception as exec:
        raise UnsupportedResponseException(f"""UnsupportedResponseException: create method response struct changed.
                    Please contact admin or use the latest agent for updates \n [Error]:
                    {str(exec)}""")


def get_cost_per_request(model_name=None, prompt_tokens=0, completion_tokens=0):
    if model_name and model_name in MODEL_COST_MAP:
        return (prompt_tokens * MODEL_COST_MAP[model_name]['prompt_cost']) + \
            (completion_tokens * MODEL_COST_MAP[model_name]['completion_cost'])
    else:
        raise UnsupportedModelException(f" unsupported model {model_name} is \
        not supported by current agent.\
        Please update the python agent or contact admin")


def _initialize_metrics(metric_prefix_path="", metric_prefix="", metric_suffix="", metric_dict=dict()):
    model_metrics_dict = dict()
    for metric_name, metric_attr in items(metric_dict):
        model_metrics_dict[metric_name] = custom_metrics_mod.CustomMetric(
            name=metric_prefix_path + METRIC_PATH_SEGREGATOR + metric_prefix + metric_name + metric_suffix,
            time_rollup_type=metric_attr[TIME_ROLLUP_STRING],
            hole_handling_type=metric_attr[HOLE_HANDLING_STRING])
    return model_metrics_dict


def _get_backend_details():
    try:
        # importing openai package since api's hostname
        # change will different api's getting hostname
        # on every exitcall
        from openai import api_base
        parsed_url = urlparse(api_base)
        port = parsed_url.port or ('443' if parsed_url.scheme == 'https' else '80')
        return (parsed_url.hostname, port, parsed_url.scheme, api_base)
    except:
        return (DEFAULT_OPENAI_ENDPOINT, '443', 'https', DEFAULT_OPENAI_ENDPOINT)


def _report_metrics(metrics_dict=None, reporting_values=None, agent=None):
    if not metrics_dict or not reporting_values:
        raise MissingReportingValuesExcepion(" Metric Reporting\
           values not found .Please provide proper method arguments\
        ")
    try:
        for metric_name, metric_value in items(reporting_values):
            agent.report_custom_metric(
                metrics_dict[metric_name],
                metric_value
            )
    except Exception as exec:
        agent.logger.error("MetricReportingError: " + str(exec))
        pass


def _get_reporting_values_per_request(model_name=None, agent=None, endpoint_response=None):
    reporting_values = dict()
    # Calculating current request tokens
    try:
        reporting_values[TOKENS_METRIC_NAME] = get_tokens_per_request(
            method_response=endpoint_response,
            token_type=RESPONSE_TOTAL_TOKEN_STRING
        )
        prompt_tokens = get_tokens_per_request(
            method_response=endpoint_response,
            token_type=RESPONSE_PROMPT_STRING
        )
        completion_tokens = get_tokens_per_request(
            method_response=endpoint_response,
            token_type=RESPONSE_COMPLETION_STRING
        )
    except UnsupportedResponseException as exec:
        agent.logger.error(str(exec))
        raise

    # Calculating current request cost per model
    try:
        if prompt_tokens and completion_tokens:
            reporting_values[COST_METRIC_NAME] = get_cost_per_request(
                model_name=model_name,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
    except UnsupportedModelException as exec:
        agent.logger.error(str(exec))
    finally:
        return reporting_values


class UnsupportedModelException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"UnsupportedModelException: {self.message}"


class UnsupportedResponseException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"UnsupportedResponseException: {self.message}"


class MissingReportingValuesExcepion(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"MissingReportingValuesExcepion: {self.message}"

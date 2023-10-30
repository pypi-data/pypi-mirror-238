from akride._utils.rest.rest_client import RestClient
from akride._utils.retry_helper import get_http_retry


def default_rest_client():
    return RestClient.get_client(retry=get_http_retry())

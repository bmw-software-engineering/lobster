DATE_FORMAT = "%Y_%m_%d_%A"
TIME_FORMAT = "%H_%M"

# Disabled since pylint does not see some members of requests
# pylint: disable=no-member
import requests

REST_GET_SUCCESS = requests.codes.ok
REST_PUT_SUCCESS = requests.codes.created
REST_DELETE_SUCCESS = requests.codes.no_content
REST_GET_NOT_FOUND = requests.codes.not_found
REST_GET_ERROR = requests.codes.forbidden
REST_GATEWAY_TIMEOUT = requests.codes.gateway_timeout

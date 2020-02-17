from rest_framework import status
from rest_framework.exceptions import ValidationError


class ExternalRequestError(ValidationError):
    pass


class ExternalRequestClientError(ExternalRequestError):
    status_code = status.HTTP_400_BAD_REQUEST


class ExternalRequestServerError(ExternalRequestError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class ExternalRequestTimeoutOrUnreachable(ExternalRequestError):
    status_code = 0

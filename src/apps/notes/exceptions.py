from rest_framework import status
from rest_framework.exceptions import APIException


class TagAddLimitException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Limit of adding tags reached (6 max)"
    default_code = "tags_limit"

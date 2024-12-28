from enum import Enum


class VendorTypeEnum(str, Enum):
    PUBLIC_APIS = "PUBLIC_APIS"
    WEB_PARSER = "WEB_PARSER"


class RequestTypes(str, Enum):
    GET = "GET"
    POST = "POST"


class ValidStatusCode:
    OK = 200


class VendorNames(str, Enum):
    OXYLAB = "OXYLAB"


class SearchParamType(str, Enum):
    QP = "QP"
    BODY = "BODY"

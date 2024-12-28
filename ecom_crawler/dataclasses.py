from dataclasses import dataclass
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


@dataclass
class CategoryWiseProductUrlsS3Paths:
    keyword: str
    hash: str
    vendor_name: str

    @classmethod
    def build_file_path_from_class_params(
        cls, keyword, hash, vendor_name
    ) -> "CategoryWiseProductUrlsS3Paths":
        return cls(keyword=keyword, hash=hash, vendor_name=vendor_name)

    def get_s3_path(self):
        return f"product_urls/{self.vendor_name}/{self.keyword}/{self.hash}/"

    def write_to_s3(self):
        """
        Implement s3 write functuonality.
        Not implementing for now. just want to show use-case
        for now return true
        """
        return True

    def check_if_exists(self):
        """
        Implement check if path exists functionality
        Not implementing for now. just want to show use-case
        for now return false
        """
        return False

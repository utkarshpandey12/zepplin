from typing import List, Tuple
import requests
from ecom_crawler.dataclasses import RequestTypes, SearchParamType
from ecom_crawler.models import VendorParams, VendorResponse


class PublicApiClient:
    def crawl(self, vendor: VendorParams, keywords_list: list) -> List[str]:  # noqa
        auth, headers, querystring, body = self.prepare_vendor_request(
            vendor=vendor
        )  # noqa
        vendor_response = VendorResponse()
        responses = []

        for keyword in keywords_list:
            vendor = self.modify_requests_search_params(
                vendor=vendor, keyword=keyword
            )  # noqa
            while self.is_paginated_results_left(
                vendor=vendor, vendor_response=vendor_response
            ):
                response = requests.request(
                    vendor.request_type,
                    vendor.search_url,
                    auth=auth,
                    json=body,
                    headers=headers,
                    params=querystring,
                )
                vendor_response = VendorResponse.from_json(
                    data=response.json(), vendor=vendor
                )
                vendor = self.increment_request_search_increment_param(
                    vendor=vendor
                )  # noqa
                responses.extend(vendor_response.product_urls)

        return responses

    def prepare_vendor_request(
        self, vendor: VendorParams
    ) -> Tuple[tuple, dict, dict, dict]:
        auth_params = self.build_auth(vendor=vendor)
        headers = self.build_request_headers(vendor=vendor)
        query_params = self.build_request_query_params(vendor=vendor)
        body = self.build_request_body(vendor=vendor)

        return auth_params, headers, query_params, body

    def build_auth(self, vendor: VendorParams):
        username = vendor.auth_params.username or ""
        password = vendor.auth_params.password or ""
        if username and password:
            return (username, password)

    def build_request_headers(self, vendor: VendorParams):
        return vendor.auth_params.headers_json

    def build_request_query_params(self, vendor: VendorParams):
        return vendor.query_params

    def build_request_body(self, vendor: VendorParams):
        if vendor.request_type == RequestTypes.GET:
            return {}
        if vendor.request_type == RequestTypes.POST:
            return vendor.body

    def modify_requests_search_params(
        self, vendor: VendorParams, keyword: str
    ) -> VendorParams:
        if vendor.search_params_type == SearchParamType.BODY:
            vendor.body[vendor.search_param_name] = keyword
        return vendor

    def increment_request_search_increment_param(
        self, vendor: VendorParams
    ) -> VendorParams:
        if vendor.search_increment_param_type == SearchParamType.BODY:
            vendor.body[vendor.search_increment_param_name] += 1

        return vendor

    def is_paginated_results_left(
        self, vendor: VendorParams, vendor_response: VendorResponse
    ) -> bool:
        if vendor.search_increment_param_type == SearchParamType.BODY:
            return vendor_response.stop_value <= vendor.body.get(
                vendor.search_increment_param_name
            )

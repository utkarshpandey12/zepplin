from typing import List, Optional, Tuple

import time
import requests

from ecom_crawler.config import ApiClientConfig
from ecom_crawler.dataclasses import RequestTypes, SearchParamType
from ecom_crawler.models import VendorParams, VendorResponse


class PublicApiClient:
    def __init__(
        self,
        max_requests_per_minute: Optional[int] = 60,
        max_total_requests: int = 1000,
    ):
        self.config = ApiClientConfig()
        self.max_requests_per_minute = (
            max_requests_per_minute or self.config.MAX_REQUESTS
        )
        self.max_total_requests = (
            max_total_requests or self.config.MAX_REQUESTS_PER_MINUTES
        )
        self.request_count = 0
        self.start_time = time.time()

    def crawl(self, vendor: VendorParams, keyword: str) -> List[str]:  # noqa
        auth, headers, querystring, body = self.prepare_vendor_request(
            vendor=vendor
        )  # noqa
        vendor_response = VendorResponse()

        vendor = self.modify_requests_search_params(
            vendor=vendor, keyword=keyword
        )  # noqa
        while self.is_paginated_results_left(
            vendor=vendor, vendor_response=vendor_response
        ):
            self._enforce_request_limits()
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

        return vendor_response.product_urls

    def _enforce_request_limits(self):
        if self.request_count >= self.max_total_requests:
            raise Exception("Maximum total request limit exceeded.")

        elapsed_time = time.time() - self.start_time
        if elapsed_time < 60 and self.request_count >= self.max_requests_per_minute:
            sleep_time = 60 - elapsed_time
            print(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds.")
            time.sleep(sleep_time)
            self.start_time = time.time()
            self.request_count = 0

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

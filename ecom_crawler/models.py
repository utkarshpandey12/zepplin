import logging
from typing import List, Optional

from pydantic import BaseModel, Field

from ecom_crawler.dataclasses import VendorNames

logger = logging.getLogger("airflow.task")


class AuthParams(BaseModel):
    headers_json: dict
    username: Optional[str]
    password: Optional[str]

    @classmethod
    def from_json(cls, data):
        return cls(
            headers_json=data.get("headers_json"),
            username=data.get("username"),
            password=data.get("password"),
        )


class VendorParams(BaseModel):
    vendor_name: str
    vendor_type: str
    search_url: str
    request_type: str
    auth_params: AuthParams
    query_params: dict
    search_params_type: str
    search_param_name: str
    search_increment_param_type: str
    search_increment_param_name: str
    vendor_host_prefix: str
    body: dict

    @classmethod
    def from_json(cls, data: dict) -> List["VendorParams"]:
        vendors_list = []
        for key, value in data.items():
            vendors_list.append(
                cls(
                    vendor_name=key,
                    vendor_type=value.get("vendor_type"),
                    search_url=value.get("search_url"),
                    auth_params=AuthParams.from_json(
                        data=value.get("auth_params")
                    ),  # noqa
                    query_params=value.get("query_params"),
                    request_type=value.get("request_type"),
                    body=value.get("body"),
                    search_params_type=value.get("search_params_type"),
                    search_param_name=value.get("search_param_name"),
                    search_increment_param_type=value.get(
                        "search_increment_param_type"
                    ),
                    search_increment_param_name=value.get(
                        "search_increment_param_name"
                    ),
                    vendor_host_prefix=value.get("vendor_host_prefix"),
                )
            )
        return vendors_list


class VendorResponse(BaseModel):
    response_json: Optional[dict] = Field(default_factory=dict)
    stop_value: Optional[int] = 0
    product_urls: List[str] = Field(default_factory=list)

    @classmethod
    def from_json(cls, data: dict, vendor: VendorParams) -> "VendorResponse":
        if vendor.vendor_name == VendorNames.OXYLAB:
            product_links = []
            for content in data["results"]:
                for _, products in content["content"]["results"].items():
                    if len(products) > 0:
                        for product in products:
                            product_links.append(product.get("url"))

            return cls(
                response_json=data,
                stop_value=data["results"][0]["content"]["last_visible_page"],
                product_urls=product_links,
            )


class VendorProductUrlsResponse(BaseModel):
    producturls: List[str] = Field(default_factory=list)
    vendor_name: str

    @classmethod
    def from_json(
        cls, product_urls: List[str], vendor: VendorParams
    ) -> "VendorProductUrlsResponse":
        modifield_product_urls = []
        for urls in product_urls:
            urls = vendor.vendor_host_prefix + urls
            modifield_product_urls.append(urls)
        return cls(producturls=modifield_product_urls, vendor_name=vendor.vendor_name)

    def to_json(self):
        return {self.vendor_name: self.producturls}

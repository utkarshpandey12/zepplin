from typing import List
from ecom_crawler.models import VendorParams
from ecom_crawler.dataclasses import VendorTypeEnum
from ecom_crawler.public_api_client import PublicApiClient
from tasks.crawler_params import get_keyword_var


class EcomCrawler:

    def __init__(self, vendor_params_json):
        self.vendor_params_json = vendor_params_json
        self.public_api_client = PublicApiClient()

    def get_vendors(self) -> List[VendorParams]:
        return VendorParams.from_json(self.vendor_params_json)

    def get_search_keywords(self) -> List[str]:
        keyword_list = get_keyword_var()
        return keyword_list

    def crawl(self) -> List[str]:
        product_urls = []
        for vendor in self.get_vendors():
            if vendor.vendor_type == VendorTypeEnum.PUBLIC_APIS:
                product_urls.extend(
                    self.public_api_client.crawl(
                        vendor=vendor, keywords_list=self.get_search_keywords()
                    )
                )

        return product_urls

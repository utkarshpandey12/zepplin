from typing import List

from ecom_crawler.dataclasses import CategoryWiseProductUrlsS3Paths, VendorTypeEnum
from ecom_crawler.models import VendorParams, VendorProductUrlsResponse
from ecom_crawler.public_api_client import PublicApiClient
from ecom_crawler.utils import compute_content_hash
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
                for keyword in self.get_search_keywords():
                    urls = self.public_api_client.crawl(vendor=vendor, keyword=keyword)

                    vendor_product_urls = VendorProductUrlsResponse.from_json(
                        product_urls=urls, vendor=vendor
                    )
                    product_urls_json = vendor_product_urls.to_json()
                    product_urls_content_hash = compute_content_hash(
                        content=product_urls_json
                    )
                    category_product_urls_paths = CategoryWiseProductUrlsS3Paths.build_file_path_from_class_params(
                        keyword=keyword,
                        hash=product_urls_content_hash,
                        vendor_name=vendor.vendor_name,
                    )
                    if not category_product_urls_paths.check_if_exists():
                        category_product_urls_paths.write_to_s3()

                    product_urls.extend(vendor_product_urls.producturls)

        return product_urls

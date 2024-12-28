from typing import Dict, List

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from ecom_crawler.crawler import EcomCrawler


class CrawlVendorsOperator(BaseOperator):
    template_fields = ("run_params",)

    @apply_defaults
    def __init__(self, run_params: Dict, **kwargs):
        self.run_params = run_params
        self.ecom_crawler = EcomCrawler(vendor_params_json=run_params)
        super().__init__(**kwargs)

    def execute(self, context: Dict) -> List[str]:
        return self.ecom_crawler.crawl()

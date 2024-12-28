import os
import sys

import pendulum
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

from operators.crawler import CrawlVendorsOperator
from tasks.crawler_params import get_vendors

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir)
)  # noqa
sys.path.append(PROJECT_ROOT)


def create_ecom_crawler_dag():
    args = {
        "owner": "airflow",
        "retries": 1,
    }
    dag = DAG(
        dag_id="e_com_crawler",
        default_args=args,
        start_date=pendulum.datetime(2024, 6, 1, tz="UTC"),
        catchup=False,
        tags=["crawler", "product_links"],
        params={"test_param": "param"},
        max_active_runs=1,
    )

    with dag:
        get_run_parameters = PythonOperator(
            task_id="get_run_parameters", python_callable=get_vendors
        )

        with TaskGroup("crawl_vendors_group") as crawl_vendors_group:
            CrawlVendorsOperator.partial(
                task_id="crawl_vendors_operator",
            ).expand(run_params=get_run_parameters.output)

        get_run_parameters >> crawl_vendors_group

    return dag


ecom_crawler = create_ecom_crawler_dag()

# Zepplin E-Commerce Crawler

This project provides a framework to crawl e-commerce websites such as Amazon or Flipkart using their public APIs. For each vendor
the tasks are scheduled in parallel  controlled by pool slots and airflow core parallelism. At the end results can be ingested into
appropriate search database by using Ingestion Operator defined in the code. Product urls json can be stored in s3 paths which are seperated by a unique main hash generated at the time of each crawler run and vendor name in the path. Each individual vendor response can also be stored under s3 based on hash generated based on content of the response. This will help eliminate already processed responses based on hash similiarity.

## Features

- Modular architecture for adding and managing multiple vendors.
- S3 paths structured in format product_urls/{vendor}/{category_keyword}/hash/urls.json
- Dynamic crawling parameters via Airflow Variables.
- Seamless integration with vendors public APIs using generic client
- Supports pagination and dynamic query generation.

---

## Directory Structure

```plaintext
ecom_crawler/
├── __init__.py
├── models.py          # Defines data models for vendors and responses.
├── dataclasses.py     # Enumerations for request types and vendor configurations.
├── operators/
│   ├── __init__.py
│   ├── crawler.py      # Airflow operator to execute vendor crawling.
├── tasks/
│   ├── __init__.py
│   ├── crawler_params.py # Helper tasks for fetching vendor and keyword variables.
├── public_api_client.py # Main client for handling API requests and pagination.
dags/
├── __init__.py
├── crawl.py           # Airflow DAG to orchestrate the crawling process.
```

## Prerequisites
- Python: Make sure Python 3.8+ is installed.
- Apache Airflow: Set up and configure Apache Airflow (2.0+ recommended).
- Environment Variables: Set up the following Airflow variables:
   - vendors: JSON configuration for the vendors to crawl
   - search_keyword_list: List of keywords for search.


## Installation
- Clone the repository:

```
git clone <repository_url>
cd ecom_crawler
```

- Install and run airflow with dependencies

```
# Airflow needs a home. `~/airflow` is the default, but you can put it
# somewhere else if you prefer (optional)
export AIRFLOW_HOME=~/airflow

# Install Airflow using the constraints file
AIRFLOW_VERSION=2.3.0
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
# For example: 3.7
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example: https://raw.githubusercontent.com/apache/airflow/constraints-2.3.0/constraints-3.7.txt
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# The Standalone command will initialise the database, make a user,
# and start all components for you.
airflow standalone

# Visit localhost:8080 in the browser and use the admin account details
# shown on the terminal to login.
# Enable the example_bash_operator dag in the home page
```

- Add Airflow variables:

  - vendors:
  ```
    {
  "OXYLAB": {
    "vendor_type": "PUBLIC_APIS",
    "search_url": "https://realtime.oxylabs.io/v1/queries",
    "request_type": "POST",
    "search_params_type": "BODY",
    "search_param_name": "query",
    "search_increment_param_type": "BODY",
    "search_increment_param_name": "start_page",
    "vendor_host_prefix": "https://amazon.com",
    "query_params": {},
    "auth_params": {
      "headers_json": {},
      "username": "amazon_products_GJzNT",
      "password": "Utkarsh+1234"
    },
    "body": {
      "source": "amazon_search",
      "domain": "nl",
      "query": "nirvana tshirt",
      "start_page": 1,
      "pages": 1,
      "parse": true
        }
    }
    }
    ```

    - search_keyword_list
    ```
    {
    "search_list": ["deodrants"]
    }

    ```


## Code Workflow
- models.py
    Defines data models using Pydantic:
    AuthParams: Handles API authentication parameters.
    VendorParams: Contains vendor-specific configurations like search_url, auth_params, and query_params.
    VendorResponse: Manages the response parsing for products.

- dataclasses.py
    Defines enumerations for request types (GET, POST), vendor types, and search parameter configurations.

- public_api_client.py
    Handles API requests and pagination:

- Constructs requests with headers, authentication, and query parameters.
    Iterates through paginated results to fetch all product URLs.

- tasks/crawler_params.py
    Fetches vendors and keywords from Airflow Variables for dynamic DAG execution.

- dags/crawl.py
    Defines the Airflow DAG:Groups tasks create parallel vendor executions

- Request Initialization:
    Authentication, headers, query parameters, and body are prepared using PublicApiClient.

-  Response Handling:
    Products and pagination data are extracted using VendorResponse.
    Pagination: Iteratively increments page numbers until all results are fetched.

from airflow.models import Variable


def get_vendors():
    vendors = []
    vendor_var = "vendors"
    vendors_json = Variable.get(
        vendor_var, deserialize_json=True, default_var={}
    )  # noqa
    for vendor, vendor_params in vendors_json.items():
        vendors.append({vendor: vendor_params})
    return vendors


def get_keyword_var():
    search_keyword_var = "search_keyword_list"

    search_keyword_json = Variable.get(
        search_keyword_var, deserialize_json=True, default_var={}
    )

    return search_keyword_json.get("search_list")

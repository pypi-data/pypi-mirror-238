import os
import requests
import tempfile
import sys
from feast import FeatureStore
from datetime import datetime
from constants import CommonService


def main():
    import time
    print("The time of code execution begin is : ", time.ctime())
    # time.sleep()
    print("The time of code will begin now")

    frequency = os.getenv("frequency")
    print("frequency - ", frequency)

    store_name = os.getenv("store_name")  # "Test_snow_30_oct_2"
    url = CommonService.base_url + CommonService.feature_store.format(store_name)
    # token = os.getenv("TOKEN")

    # headers = {
    #     "Authorization": 'token {}'.format(token)
    # }

    headers = {
        "accept": "application/json",
        "X-Project-Id": os.getenv("PROJECT_ID"),
        'X-Auth-Userid': os.getenv("userId"),
        'X-Auth-Username': os.getenv("userId"),
        'X-Auth-Email': os.getenv("userId"),
    }

    response = requests.get(url=url,
                            headers=headers,
                            verify=False)

    print("store_obj - ", response)
    temp_dir = tempfile.mkdtemp()

    yaml_path = os.path.join(temp_dir, "feature_store.yaml")

    if response.status_code == 200:
        # Parse the JSON response
        with open(yaml_path, 'wb') as f:
            f.write(response.content)

    store_materialize(temp_dir)

    print("Inside feature store recipe code", frequency)

    return "OK"


def store_materialize(yaml_path):
    print("Inside store_materialize \n")
    print("yaml_path", yaml_path)
    store = FeatureStore(repo_path=yaml_path)

    report_path = os.path.join(os.getenv("output_path"), f"{os.getenv('plugin_type')}.txt")
    print("Output path is - ", report_path)

    # Open the output file for writing
    with open(report_path, "w") as file:
        # Redirect the standard output to the file
        sys.stdout = file

        # Define a method to perform materialization
        store.materialize_incremental(end_date=datetime.now())

    # alert_data_path = os.path.join(os.getenv("output_path"), "alert_data.json")

    return "OK"


if __name__ == "__main__":
    main()

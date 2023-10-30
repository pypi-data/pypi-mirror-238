import os
import requests


def main():
    frequency = os.getenv("frequency")
    print("frequency - ", frequency)
    store_name = "Test_snow_30_oct_2"
    url = f"https://dev.refract-fosfor.com/refract/common/api/v1/get_feature_store/?feature_store_name={store_name}"
    token = os.getenv("TOKEN")
    headers = {
        "X-Auth-Username": os.getenv("userId"),
        "X-Auth-Userid": os.getenv("userId"),
        # "X-Auth-Email": g.useremail,
        "X-Project-Id": os.getenv("PROJECT_ID"),
        "Authorization": 'token {}'.format(token)
    }

    store_obj = requests.get(url=url,
                             headers=headers,
                             verify=False)
    print("store_obj - ", store_obj)

    # read env data
    # get token
    # call refract common service for fs object details
    # create fs object and yaml
    # run materialize command
    # get the result
    # store the result

    print("Inside feature store recipe code", frequency)

    return "OK"


if __name__ == "__main__":
    main()

import os
import requests
import jsonpickle


def main():
    import time
    print("The time of code execution begin is : ", time.ctime())
    time.sleep(600)
    print("The time of code will begin now")

    frequency = os.getenv("frequency")
    print("frequency - ", frequency)
    store_name = "Test_snow_30_oct_2"
    url = f"https://dev.refract-fosfor.com/refract/common/api/v1/get_feature_store/?feature_store_name={store_name}"
    token = os.getenv("TOKEN")
    headers = {
        "accept": "application/json",
        "X-Auth-Username": os.getenv("userId"),
        "X-Auth-Userid": os.getenv("userId"),
        # "X-Auth-Email": g.useremail,
        "X-Project-Id": os.getenv("PROJECT_ID"),
        "Authorization": 'token {}'.format(token)
    }

    response = requests.get(url=url,
                            headers=headers,
                            verify=False)
    print("store_obj - ", response.json())

    # store_json = jsonpickle.encode(response.json(), unpicklable=False)
    store = jsonpickle.decode(response.json())
    print("store object - ", store)

    store_materialize(store)

    # read env data
    # get token
    # call refract common service for fs object details
    # create fs object and yaml
    # run materialize command
    # get the result
    # store the result

    print("Inside feature store recipe code", frequency)

    return "OK"


def store_materialize(store):
    from datetime import datetime
    materialize = store.materialize_incremental(end_date=datetime.utcnow())

    print("materialize logs- ", materialize)
    return "OK"


if __name__ == "__main__":
    main()

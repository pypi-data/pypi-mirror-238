import os

BASE_DIR = os.getcwd()


class CommonService:
    base_url = "http://refract-common-service:5000/refract/common/api"
    feature_store = "/v1/get_feature_store/?feature_store_name={}"

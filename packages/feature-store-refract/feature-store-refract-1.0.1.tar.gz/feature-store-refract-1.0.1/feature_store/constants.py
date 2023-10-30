import os

BASE_DIR = os.getcwd()


class ModelConstants:
    MODEL_DIR = os.path.join(BASE_DIR, "datasource")
    MODEL_FILE = "ml_model"
    SCORING_FUN = "scoring_func"
    MODELS_PATH = "/models"

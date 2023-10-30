import json
from pyflare.utils.helper import get_content, constants
from pyspark.sql.session import SparkSession

GCS_JSON_FILE_EMAIL = "client_email"
GCS_JSON_FILE_PRIVATE_KEY = "private_key"
GCS_JSON_FILE_PRIVATE_KEY_ID = "private_key_id"

SPARK_CONF_GCS_EMAIL = "fs.gs.auth.service.account.email"
SPARK_CONF_GCS_PRIVATE_KEY = "fs.gs.auth.service.account.private.key"
SPARK_CONF_GCS_PRIVATE_KEY_ID = "fs.gs.auth.service.account.private.key.id"


def get_spark_conf(secret_res: dict, properties: dict):
    conf = dict()
    gcs_key_file_name = properties.get(constants.GCS_KEY_JSON)
    if gcs_key_file_name is None:
        raise Exception("Key: {0} not found in properties file".format(constants.GCS_KEY_JSON))

    gcs_json = json.loads(get_content(gcs_key_file_name, secret_res))

    conf[SPARK_CONF_GCS_EMAIL] = get_value_or_throw(GCS_JSON_FILE_EMAIL, gcs_json)
    conf[SPARK_CONF_GCS_PRIVATE_KEY] = get_value_or_throw(GCS_JSON_FILE_PRIVATE_KEY, gcs_json)
    conf[SPARK_CONF_GCS_PRIVATE_KEY_ID] = get_value_or_throw(GCS_JSON_FILE_PRIVATE_KEY_ID, gcs_json)
    return conf


def has_spark_secrets(spark: SparkSession):
    try:
        spark.conf.get(SPARK_CONF_GCS_EMAIL)
        spark.conf.get(SPARK_CONF_GCS_PRIVATE_KEY)
        spark.conf.get(SPARK_CONF_GCS_PRIVATE_KEY_ID)
        return True
    except Exception:
        return False


def get_value_or_throw(key: str, data: dict):
    if data[key] is None:
        raise Exception("Key: {0} not found in gcs properties".format(key))
    return data[key]

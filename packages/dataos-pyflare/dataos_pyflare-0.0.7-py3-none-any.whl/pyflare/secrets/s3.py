from pyspark.sql.session import SparkSession

S3_JSON_FILE_ACCESS_KEY_ID = "awsaccesskeyid"
S3_JSON_FILE_SECRET_KEY = "awssecretaccesskey"

SPARK_CONF_S3_ACCESS_KEY_ID = "fs.s3a.access.key"
SPARK_CONF_S3_SECRET_KEY = "fs.s3a.secret.key"


def get_spark_conf(properties: dict):
    conf = dict()
    s3_access_key_id = get_value_or_throw(S3_JSON_FILE_ACCESS_KEY_ID, properties)
    s3_secret_key = get_value_or_throw(S3_JSON_FILE_SECRET_KEY, properties)
    conf[SPARK_CONF_S3_ACCESS_KEY_ID] = s3_access_key_id
    conf[SPARK_CONF_S3_SECRET_KEY] = s3_secret_key
    return conf


def has_spark_secrets(spark: SparkSession):
    try:
        spark.conf.get(SPARK_CONF_S3_ACCESS_KEY_ID)
        spark.conf.get(SPARK_CONF_S3_SECRET_KEY)
        return True
    except Exception:
        return False


def get_value_or_throw(key: str, data: dict):
    if data[key] is None:
        raise Exception("Key: {0} not found in s3 properties".format(key))
    return data[key]

from pyflare.secrets import gcs, abfss
from pyflare.secrets import s3

from pyflare.utils.helper import get_content, get_properties
from pyspark.sql.session import SparkSession

DEPOT_TYPE_GCS = "GCS"
DEPOT_TYPE_S3 = "S3"
DEPOT_TYPE_ABFSS = "ABFSS"
DEPOT_TYPE_FILE = "FILE"


def load(depot_name: str, depot_type: str, secret_res: dict):
    depot_file_content = get_content(depot_name, secret_res)
    properties = get_properties(depot_file_content)

    if depot_type == DEPOT_TYPE_GCS:
        return gcs.get_spark_conf(secret_res, properties)
    if depot_type == DEPOT_TYPE_S3:
        return s3.get_spark_conf(properties)
    if depot_type == DEPOT_TYPE_ABFSS:
        return abfss.get_spark_conf(properties)
    else:
        raise Exception("Depot type not supported!!")


def is_secrets_loaded(depot_type: str, spark: SparkSession):
    if depot_type == DEPOT_TYPE_GCS:
        return gcs.has_spark_secrets(spark)
    if depot_type == DEPOT_TYPE_S3:
        return s3.has_spark_secrets(spark)
    if depot_type == DEPOT_TYPE_ABFSS:
        return False
    if depot_type == DEPOT_TYPE_FILE:
        return True
    else:
        raise Exception("Depot type not supported!!")

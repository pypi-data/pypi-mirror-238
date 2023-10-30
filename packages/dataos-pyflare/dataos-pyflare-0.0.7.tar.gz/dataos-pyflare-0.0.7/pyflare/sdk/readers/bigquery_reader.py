import base64
import json

from pyflare.sdk.config.constants import GCS_ACCOUNT_EMAIL, GCS_PROJECT_ID, GCS_ACCOUNT_PRIVATE_KEY, \
    GCS_ACCOUNT_PRIVATE_KEY_ID, GCS_AUTH_ACCOUNT_ENABLED
from pyflare.sdk.config.read_config import ReadConfig
from pyflare.sdk.readers.file_reader import Reader
from pyflare.sdk.utils import pyflare_logger, generic_utils


class BigqueryInputReader(Reader):

    def __init__(self, read_config: ReadConfig):
        super().__init__(read_config)
        self.log = pyflare_logger.get_pyflare_logger(name=__name__)

    def read(self):
        spark_options = self.read_config.spark_options
        io_format = self.read_config.io_format
        dataset_path = generic_utils.get_dataset_path(self.read_config)
        if spark_options:
            df = self.spark.read.options(**spark_options).format(io_format).load(dataset_path)
        else:
            df = self.spark.read.format(io_format).load(dataset_path)
        return df

    def read_stream(self):
        pass

    def get_conf(self):
        # depot_name = self.read_config.depot_details['depot']
        # secret_file_path = f"{depot_name}_secrets_file_path"
        # keyfile_path = self.read_config.depot_details.get("secrets", {}).get(secret_file_path, "")

        connection_details = self.read_config.depot_details.get("connection", {})
        secrets = self.read_config.depot_details.get("secrets", {})
        encoded_secrets = base64.b64encode(json.dumps(secrets).encode('utf-8')).decode('utf-8')
        bigquery_spark_option = {
            "parentProject": connection_details.get("project", ""),
            "dataset": self.read_config.collection(),
            "table": self.read_config.dataset_name()
        }
        self.read_config.spark_options = bigquery_spark_option
        bigquery_conf = [
            # ("spark.hadoop.google.cloud.auth.service.account.json.keyfile", keyfile_path),
            ("credentials", encoded_secrets),
            (GCS_AUTH_ACCOUNT_ENABLED, "true"),
            (GCS_ACCOUNT_EMAIL, secrets.get("client_email", "")),
            (GCS_PROJECT_ID, secrets.get("project_id", "")),
            (GCS_ACCOUNT_PRIVATE_KEY, secrets.get("private_key", "")),
            (GCS_ACCOUNT_PRIVATE_KEY_ID, secrets.get("private_key_id", "")),
            ("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem"),
            ("spark.hadoop.fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS"),
        ]
        return bigquery_conf

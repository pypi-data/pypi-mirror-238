import base64
import json

from pyflare.sdk.config.constants import GCS_AUTH_ACCOUNT_ENABLED, GCS_ACCOUNT_EMAIL, GCS_PROJECT_ID, \
    GCS_ACCOUNT_PRIVATE_KEY, GCS_ACCOUNT_PRIVATE_KEY_ID
from pyflare.sdk.config.write_config import WriteConfig
from pyflare.sdk.utils import pyflare_logger
from pyflare.sdk.writers.writer import Writer


class BigqueryOutputWriter(Writer):

    def __init__(self, write_config: WriteConfig):
        super().__init__(write_config)
        self.log = pyflare_logger.get_pyflare_logger(name=__name__)

    def write(self, df):
        # self.resolve_write_format()
        if self.write_config.is_stream:
            return self.write_stream()
        spark_options = self.write_config.spark_options
        # df = self.spark.sql(f"select * from {self.view_name}")
        df.write.options(**spark_options).format("bigquery").mode(self.write_config.mode).save()

    def write_stream(self):
        pass

    def get_conf(self):
        # depot_name = self.write_config.depot_details['depot']
        # secret_file_path = f"{depot_name}_secrets_file_path"
        # keyfile_path = self.write_config.depot_details.get("secrets", {}).get(secret_file_path, "")

        connection_details = self.write_config.depot_details.get("connection", {})
        secrets = self.write_config.depot_details.get("secrets", {})
        encoded_secrets = base64.b64encode(json.dumps(secrets).encode('utf-8')).decode('utf-8')
        bigquery_spark_option = {
            "parentProject": connection_details.get("project", ""),
            "dataset": self.write_config.collection(),
            "table": self.write_config.dataset_name()
        }
        self.write_config.spark_options = bigquery_spark_option

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

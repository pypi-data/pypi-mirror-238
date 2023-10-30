from pyflare.sdk.config.constants import ELASTIC_SEARCH_IO_FORMAT
from pyflare.sdk.config.write_config import WriteConfig
from pyflare.sdk.utils import pyflare_logger
from pyflare.sdk.writers.writer import Writer


class ElasticSearchOutputWriter(Writer):

    def __init__(self, write_config: WriteConfig):
        super().__init__(write_config)
        self.log = pyflare_logger.get_pyflare_logger(name=__name__)

    def write(self, df):
        # self.resolve_write_format()
        if self.write_config.is_stream:
            return self.write_stream()
        spark_options = self.write_config.spark_options
        # df = self.spark.sql(f"select * from {self.view_name}")
        df.write.format(ELASTIC_SEARCH_IO_FORMAT).mode(self.write_config.mode).options(**spark_options).save()

    def write_stream(self):
        pass

    def get_conf(self):
        es_spark_options = {
            "es.nodes": self.write_config.depot_details.get('connection', {}).get('nodes', "")[0],
            "es.resource": self.write_config.dataset_name(),
            "es.nodes.wan.only": True,
            "es.net.http.auth.user": self.write_config.depot_details.get('secrets', {}).get('username', ""),
            "es.net.http.auth.pass": self.write_config.depot_details.get('secrets', {}).get('password', ""),
            "es.nodes.discovery": False
        }
        self.write_config.spark_options = es_spark_options
        return list()

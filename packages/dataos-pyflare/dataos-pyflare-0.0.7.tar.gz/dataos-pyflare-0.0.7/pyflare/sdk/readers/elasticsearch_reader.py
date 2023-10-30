from pyflare.sdk.config.constants import ELASTIC_SEARCH_IO_FORMAT
from pyflare.sdk.config.read_config import ReadConfig
from pyflare.sdk.readers.file_reader import Reader
from pyflare.sdk.utils import pyflare_logger, generic_utils


class ElasticSearchInputReader(Reader):

    def __init__(self, read_config: ReadConfig):
        super().__init__(read_config)
        self.log = pyflare_logger.get_pyflare_logger(name=__name__)

    def read(self):
        spark_options = self.read_config.spark_options
        io_format = self.read_config.io_format
        dataset_path = generic_utils.get_dataset_path(self.read_config)
        if spark_options:
            df = self.spark.read.format(ELASTIC_SEARCH_IO_FORMAT).options(**spark_options).load(dataset_path)
        else:
            df = self.spark.read.format(ELASTIC_SEARCH_IO_FORMAT).load(dataset_path)
        return df

    def read_stream(self):
        pass

    def get_conf(self):
        es_spark_options = {
            "es.nodes": self.read_config.depot_details.get('connection', {}).get('nodes', "")[0],
            "es.resource": self.read_config.dataset_name(),
            "es.nodes.wan.only": True,
            "es.net.http.auth.user": self.read_config.depot_details.get('secrets', {}).get('username', ""),
            "es.net.http.auth.pass": self.read_config.depot_details.get('secrets', {}).get('password', ""),
            "es.nodes.discovery": False
        }
        self.read_config.spark_options = es_spark_options
        return list()

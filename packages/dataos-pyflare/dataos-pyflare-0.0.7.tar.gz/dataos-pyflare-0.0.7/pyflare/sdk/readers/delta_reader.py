import ast
import base64

from pyflare.sdk.config import constants
from pyflare.sdk.config.read_config import ReadConfig
from pyflare.sdk.readers.file_reader import FileInputReader
from pyflare.sdk.utils import pyflare_logger, generic_utils


class DeltaInputReader(FileInputReader):
    DELTA_CONF = '''[
            ("spark.sql.catalog.spark_catalog","org.apache.spark.sql.delta.catalog.DeltaCatalog"),
            ("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        ]'''

    def __init__(self, read_config: ReadConfig):
        super().__init__(read_config)
        self.log = pyflare_logger.get_pyflare_logger(__name__)

    def read(self):
        spark_options = self.read_config.spark_options
        io_format = self.read_config.io_format
        dataset_path = self.read_config.dataset_absolute_path()
        if spark_options:
            df = self.spark.read.options(**spark_options).format(io_format).load(dataset_path)
        else:
            df = self.spark.read.format(io_format).load(dataset_path)
        return df

    def read_stream(self):
        pass

    def get_conf(self):
        self.log.debug("calling : ", f"_{self.read_config.depot_type()}_{self.read_config.io_format}")
        return getattr(self, f"_{self.read_config.depot_type()}_{self.read_config.io_format}")()

    def _abfss_delta(self):
        delta_conf = ast.literal_eval(self.DELTA_CONF.format(catalog_name=self.read_config.depot_name()))
        delta_conf.extend(generic_utils.get_abfss_spark_conf(self.read_config))
        return delta_conf

    def _get_dataset_path(self):
        return "{}.{}.{}".format(self.read_config.depot_name(), self.read_config.collection(),
                                 self.read_config.dataset_name())

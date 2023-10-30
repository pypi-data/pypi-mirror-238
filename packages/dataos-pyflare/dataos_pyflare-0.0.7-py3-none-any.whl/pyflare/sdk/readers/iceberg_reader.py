import ast

from pyflare.sdk.config.constants import S3_ICEBERG_FILE_IO
from pyflare.sdk.config.read_config import ReadConfig
from pyflare.sdk.readers.file_reader import FileInputReader
from pyflare.sdk.utils import pyflare_logger, generic_utils


class IcebergInputReader(FileInputReader):
    ICEBERG_CONF = '''[
            ("spark.sql.catalog.{catalog_name}", "org.apache.iceberg.spark.SparkCatalog"),
            ("spark.sql.catalog.{catalog_name}.type", "hadoop"),
            ("spark.sql.catalog.{catalog_name}.warehouse", "{depot_base_path}")
        ]'''
    
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
        self.log.debug(f"calling : _{self.read_config.depot_type()}_{self.read_config.io_format}")
        return getattr(self, f"_{self.read_config.depot_type()}_{self.read_config.io_format}")()
    
    def _abfss_iceberg(self):
        dataset_absolute_path = self.read_config.dataset_absolute_path()
        # depot_base_path = dataset_absolute_path.split(self.read_config.collection())[0] if self.read_config.collection() else dataset_absolute_path
        iceberg_conf = ast.literal_eval(self.ICEBERG_CONF.format(catalog_name=self.read_config.depot_name(),
                                                                 depot_base_path=dataset_absolute_path))
        iceberg_conf.extend(generic_utils.get_abfss_spark_conf(self.read_config))
        return iceberg_conf

    def _s3_iceberg(self):
        dataset_absolute_path = self.read_config.dataset_absolute_path()
        # depot_base_path = dataset_absolute_path.split(self.read_config.collection())[0]
        iceberg_conf = ast.literal_eval(self.ICEBERG_CONF.format(catalog_name=self.read_config.depot_name(),
                                                                 depot_base_path=dataset_absolute_path))
        iceberg_conf.append(S3_ICEBERG_FILE_IO)
        iceberg_conf.extend(generic_utils.get_s3_spark_conf(self.read_config))
        return iceberg_conf

    def _gcs_iceberg(self):
        dataset_absolute_path = self.read_config.dataset_absolute_path()
        # depot_base_path = dataset_absolute_path.split(self.read_config.collection())[0]
        iceberg_conf = ast.literal_eval(self.ICEBERG_CONF.format(catalog_name=self.read_config.depot_name(),
                                                                 depot_base_path=dataset_absolute_path))
        iceberg_conf.extend(generic_utils.get_gcs_spark_conf(self.read_config))
        return iceberg_conf

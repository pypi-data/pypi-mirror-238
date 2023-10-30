from pyflare.sdk.config.read_config import ReadConfig
from pyflare.sdk.readers.reader import Reader
from pyflare.sdk.utils import pyflare_logger, generic_utils


class FileInputReader(Reader):
    
    def __init__(self, read_config: ReadConfig):
        super().__init__(read_config)
        self.log = pyflare_logger.get_pyflare_logger(name=__name__)
    
    def read(self):
        if self.read_config.is_stream:
            return self.read_stream()
        spark_options = self.read_config.spark_options
        io_format = self.read_config.io_format
        dataset_path = self.read_config.dataset_absolute_path()
        if spark_options:
            df = self.spark.read.options(**spark_options).format(io_format).load(dataset_path)
        else:
            df = self.spark.read.format(io_format).load(dataset_path)
        return df
    
    def read_stream(self):
        return getattr(self, f"_read_stream_{self.read_config.io_format}")()
    
    def get_conf(self):
        return getattr(self, f"_{self.read_config.depot_type()}")()

    def _abfss(self):
        spark_conf = generic_utils.get_abfss_spark_conf(self.read_config)
        return spark_conf

    def _s3(self):
        spark_conf = generic_utils.get_s3_spark_conf(self.read_config)
        return spark_conf

    def _gcs(self):
        spark_conf = generic_utils.get_gcs_spark_conf(self.read_config)
        return spark_conf

    def _read_csv(self):
        pass
    
    def _read_json(self):
        pass
    
    def _read_parquet(self):
        pass
    
    def _read_stream_csv(self):
        pass
    
    def _read_stream_json(self):
        pass
    
    def _read_stream_parquet(self):
        pass

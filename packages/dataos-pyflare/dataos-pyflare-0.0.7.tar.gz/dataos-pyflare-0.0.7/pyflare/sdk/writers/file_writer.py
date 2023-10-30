from pyflare.sdk.config.write_config import WriteConfig
from pyflare.sdk.writers.writer import Writer
from pyflare.sdk.utils import pyflare_logger, generic_utils


class FileOutputWriter(Writer):
    
    def __init__(self, write_config: WriteConfig):
        super().__init__(write_config)
        self.log = pyflare_logger.get_pyflare_logger(name=__name__)
    
    def write(self, df):
        if self.write_config.is_stream:
            return self.write_stream()
        spark_options = self.write_config.spark_options
        io_format = self.write_config.io_format
        dataset_path = self.write_config.dataset_absolute_path()
        write_mode = self.write_config.mode
        if spark_options:
            df_writer = df.write.options(**spark_options)
        else:
            df_writer = df.write
        df_writer.mode(write_mode).format(io_format).save(dataset_path)
        # getattr(self, f"write_{self.write_config.io_format}")(df_writer)

    def write_stream(self):
        pass
    
    def get_conf(self):
        return getattr(self, f"_{self.write_config.depot_type()}")()

    def write_csv(self):
        pass
    
    def write_json(self):
        pass
    
    def write_parquet(self):
        pass

    def _abfss(self):
        spark_conf = generic_utils.get_abfss_spark_conf(self.write_config)
        return spark_conf

    def _s3(self):
        spark_conf = generic_utils.get_s3_spark_conf(self.write_config)
        return spark_conf

    def _gcs(self):
        self.write_config.spark_options["parentProject"] = \
            self.write_config.depot_details.get("secret", {}).get("project_id", "")

        spark_conf = generic_utils.get_gcs_spark_conf(self.write_config)
        return spark_conf

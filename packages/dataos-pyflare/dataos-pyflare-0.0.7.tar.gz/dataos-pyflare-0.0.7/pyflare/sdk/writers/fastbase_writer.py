import ast
import base64

import pyspark.sql.functions as F
from pyflare.sdk.config import constants
from pyflare.sdk.config.write_config import WriteConfig
from pyflare.sdk.utils import pyflare_logger
from pyflare.sdk.writers.file_writer import FileOutputWriter
from pyspark.sql.readwriter import DataFrameWriter


class FastBaseOutputWriter(FileOutputWriter):
    PULSAR_Options = '''[
            ("service.url", "{serviceUrl}"),
            ("admin.url", "{adminUrl}"),
            ("pulsar.admin.authPluginClassName", "org.apache.pulsar.client.impl.auth.AuthenticationToken"),
            ("pulsar.admin.authParams","token:{Apikey}"),
            ("pulsar.client.authPluginClassName","org.apache.pulsar.client.impl.auth.AuthenticationToken"),
            ("pulsar.client.authParams","token:{Apikey}"),
            ("topic","persistent://public/default/{dataset}")
        ]'''

    def __init__(self, write_config: WriteConfig):
        super().__init__(write_config)
        self.log = pyflare_logger.get_pyflare_logger(name=__name__)

    def write(self, df):
        if self.write_config.is_stream:
            return self.write_config
        return getattr(self, f"_write_{self.write_config.io_format}")(df)

    def write_stream(self):
        pass

    def get_conf(self):
        return []

    def _write_pulsar(self, df):
        from pyflare.sdk.core.session_builder import g_dataos_token
        pulsar_options = dict(ast.literal_eval(
            self.PULSAR_Options.format(serviceUrl=self.write_config.connection().get("serviceUrl"),
                                       adminUrl=self.write_config.connection().get("adminUrl"), Apikey=g_dataos_token,
                                       dataset=self.write_config.dataset_name())))
        spark_options = self.write_config.spark_options
        if spark_options:
            pulsar_options.update(spark_options)
        io_format = self.write_config.io_format
        # df = self.spark.sql(f"select * from {self.view_name}")
        df.write.options(**pulsar_options).format(io_format).save()
        return df
    
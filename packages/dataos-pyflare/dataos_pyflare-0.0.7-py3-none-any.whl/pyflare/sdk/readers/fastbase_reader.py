import ast

from pyflare.sdk.config.read_config import ReadConfig
from pyflare.sdk.readers.reader import Reader
from pyflare.sdk.utils import pyflare_logger


class FastBaseInputReader(Reader):

    PULSAR_Options = '''[
            ("service.url", "{serviceUrl}"),
            ("admin.url", "{adminUrl}"),
            ("pulsar.admin.authPluginClassName", "org.apache.pulsar.client.impl.auth.AuthenticationToken"),
            ("pulsar.admin.authParams","token:{Apikey}"),
            ("pulsar.client.authPluginClassName","org.apache.pulsar.client.impl.auth.AuthenticationToken"),
            ("pulsar.client.authParams","token:{Apikey}"),
            ("topic","persistent://public/default/{dataset}")
        ]'''

    def __init__(self, read_config: ReadConfig):
        super().__init__(read_config)
        self.log = pyflare_logger.get_pyflare_logger(name=__name__)

    def read(self):
        if self.read_config.is_stream:
            return self.read_stream()
        return getattr(self, f"_read_{self.read_config.io_format}")()

    def read_stream(self):
        return

    def get_conf(self):
        return []

    def _read_pulsar(self):
        from pyflare.sdk.core.session_builder import g_dataos_token
        pulsar_options = dict(ast.literal_eval(
            self.PULSAR_Options.format(serviceUrl=self.read_config.connection().get("serviceUrl"),
                                       adminUrl=self.read_config.connection().get("adminUrl"), Apikey=g_dataos_token,
                                       dataset=self.read_config.dataset_name())))
        spark_options = self.read_config.spark_options
        if spark_options:
            pulsar_options.update(spark_options)
        io_format = self.read_config.io_format
        df = self.spark.read.options(**pulsar_options).format(io_format).load()
        return df

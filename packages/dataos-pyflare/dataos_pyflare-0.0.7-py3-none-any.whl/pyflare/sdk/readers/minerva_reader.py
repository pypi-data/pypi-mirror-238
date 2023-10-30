from pyflare.sdk.config.read_config import ReadConfig
from pyflare.sdk.readers.reader import Reader
from pyflare.sdk.config.constants import MINEVRA_URL
from pyflare.sdk.utils import pyflare_logger


class MinervaInputReader(Reader):
    
    def __init__(self, read_config: ReadConfig):
        super().__init__(read_config)
        self.log = pyflare_logger.get_pyflare_logger(name=__name__)
    
    def read(self):
        if self.read_config.is_stream:
            return self.read_stream()
        self.log.debug(self.read_config.io_format)
        spark_options = self.get_minevra_options()
        return self.spark.read.format(self.read_config.io_format).options(**spark_options).load()
    
    def read_stream(self):
        return getattr(self, f"_read_stream_{self.read_config.io_format}")()
    
    def get_conf(self):
        return []
    
    def get_minevra_options(self):
        from pyflare.sdk.core.session_builder import g_dataos_token
        from pyflare.sdk.config.constants import DATAOS_BASE_URL
        read_options = {
            "url": MINEVRA_URL.format(DATAOS_BASE_URL),
            "driver": self.read_config.driver,
            "SSL": "true",
            "accessToken": g_dataos_token,
            "query": self.read_config.query,
            "source": "pyflare.sdk"
        }
        if self.read_config.spark_options:
            read_options.update(self.read_config.spark_options)
        return read_options
    
    
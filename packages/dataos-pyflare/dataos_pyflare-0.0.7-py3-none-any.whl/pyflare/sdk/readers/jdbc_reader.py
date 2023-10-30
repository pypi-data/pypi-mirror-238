from pyflare.sdk.config.read_config import ReadConfig
from pyflare.sdk.readers.reader import Reader
from pyflare.sdk.utils import pyflare_logger


class JDBCInputReader(Reader):
    
    def __init__(self, read_config: ReadConfig):
        super().__init__(read_config)
        self.log = pyflare_logger.get_pyflare_logger(name=__name__)
    
    def read(self):
        if self.read_config.is_stream:
            return self.read_stream()
        self.log.debug(self.read_config.io_format)
        spark_options = getattr(self, f"_{self.read_config.io_format}_read_options")()
        return self.spark.read.options(**spark_options).format("jdbc").load()
    
    def read_stream(self):
        return getattr(self, f"_read_stream_{self.read_config.io_format}")()
    
    def get_conf(self):
        return {}
    
    def _jdbc_read_options(self):
        pass
    
    def _postgresql_read_options(self):
        spark_options = self.read_config.spark_options
        secrets = self.read_config.depot_details.get("secrets")
        connection = self.read_config.connection()
        if not self.read_config.driver:
            self.read_config.driver = "org.postgresql.Driver"
        postgres_read_options = {
            "url": connection.get("url", "").split("?currentSchema=")[0],
            "dbtable": f"{self.read_config.collection()}.{self.read_config.dataset_name()}",
            "user": secrets.get("username", ""),
            "password": secrets.get("password", ""),
            "driver": self.read_config.driver
            }
        self.log.debug(f"postgres_read_options: {postgres_read_options}")
        if spark_options:
            postgres_read_options.update(spark_options)
        self.log.debug(f"Merged options: {postgres_read_options}")
        return postgres_read_options

    def _redshift_read_options(self):
        spark_options = self.read_config.spark_options
        secrets = self.read_config.depot_details.get("secrets")
        connection = self.read_config.connection()
        if not self.read_config.driver:
            self.read_config.driver = "com.amazon.redshift.jdbc.Driver"
        redshift_read_options = {
            "url": connection.get("url", ""),
            "dbtable": f"{self.read_config.collection()}.{self.read_config.dataset_name()}",
            "user": secrets.get("username", ""),
            "password": secrets.get("password", ""),
            "driver": self.read_config.driver
        }
        if spark_options:
            redshift_read_options.update(spark_options)
        self.log.info(f"Merged options: {redshift_read_options}")
        return redshift_read_options

    def _mysql_read_options(self):
        spark_options = self.read_config.spark_options
        secrets = self.read_config.depot_details.get("secrets")
        connection = self.read_config.connection()
        if not self.read_config.driver:
            self.read_config.driver = "com.mysql.jdbc.Driver"
        mysql_read_options = {
            "url": connection.get("url", ""),
            "dbtable": f"{self.read_config.collection()}.{self.read_config.dataset_name()}",
            "user": secrets.get("username", ""),
            "password": secrets.get("password", ""),
            "driver": self.read_config.driver
        }
        if spark_options:
            mysql_read_options.update(spark_options)
        self.log.debug(f"Merged options: {mysql_read_options}")
        return mysql_read_options
    
    def _oracle_read_options(self):
        pass

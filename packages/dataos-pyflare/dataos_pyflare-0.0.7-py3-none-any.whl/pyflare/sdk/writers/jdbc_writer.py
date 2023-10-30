from pyflare.sdk.config.write_config import WriteConfig
from pyflare.sdk.utils import pyflare_logger
from pyflare.sdk.writers.writer import Writer


class JDBCOutputWriter(Writer):
    
    def __init__(self, write_config: WriteConfig):
        super().__init__(write_config)
        self.log = pyflare_logger.get_pyflare_logger(name=__name__)
    
    def write(self, df):
        # self.resolve_write_format()
        if self.write_config.is_stream:
            return self.write_stream()
        spark_options = getattr(self, f"_{self.write_config.io_format}_write_options")()
        # df = self.spark.sql(f"select * from {self.view_name}")
        df.write.options(**spark_options).format("jdbc").mode(self.write_config.mode).save()
    
    def write_stream(self):
        pass
    
    def get_conf(self):
        return {}
    
    def _jdbc_write_options(self):
        pass

    def _postgres_write_options(self):
        return self._postgresql_write_options()
    
    def _postgresql_write_options(self):
        spark_options = self.write_config.spark_options
        secrets = self.write_config.depot_details.get("secrets")
        connection = self.write_config.connection()
        if not self.write_config.driver:
            self.write_config.driver = "org.postgresql.Driver"
        postgres_write_options = {
            "url": connection.get("url", "").split("?currentSchema=")[0],
            "dbtable": f"{self.write_config.collection()}.{self.write_config.dataset_name()}",
            "user": secrets.get("username", ""),
            "password": secrets.get("password", ""),
            "driver": self.write_config.driver
        }
        if spark_options:
            postgres_write_options.update(spark_options)
        self.log.info(f"Merged options: {postgres_write_options}")
        return postgres_write_options

    def _redshift_write_options(self):
        spark_options = self.write_config.spark_options
        secrets = self.write_config.depot_details.get("secrets")
        connection = self.write_config.connection()
        if not self.write_config.driver:
            self.write_config.driver = "com.amazon.redshift.jdbc.Driver"
        redshift_write_options = {
            "url": connection.get("url", ""),
            "dbtable": f"{self.write_config.collection()}.{self.write_config.dataset_name()}",
            "user": secrets.get("username", ""),
            "password": secrets.get("password", ""),
            "driver": self.write_config.driver
        }
        if spark_options:
            redshift_write_options.update(spark_options)
        self.log.info(f"Merged options: {redshift_write_options}")
        return redshift_write_options

    def _sqlserver_write_options(self):
        pass

    def _oracle_write_options(self):
        pass
    
    def _mysql_write_options(self):
        spark_options = self.write_config.spark_options
        secrets = self.write_config.depot_details.get("secrets")
        connection = self.write_config.connection()
        if not self.write_config.driver:
            self.write_config.driver = "com.mysql.jdbc.Driver"
        mysql_write_options = {
            "url": connection.get("url", ""),
            "dbtable": f"{self.read_config.collection()}.{self.read_config.dataset_name()}",
            "user": secrets.get("username", ""),
            "password": secrets.get("password", ""),
            "driver": self.write_config.driver
        }
        self.log.warn(f"mysql_write_options: {mysql_write_options}")
        self.log.debug(f"mysql_write_options: {mysql_write_options}")
        if spark_options:
            mysql_write_options.update(spark_options)
        self.log.debug(f"Merged options: {mysql_write_options}")
        return mysql_write_options

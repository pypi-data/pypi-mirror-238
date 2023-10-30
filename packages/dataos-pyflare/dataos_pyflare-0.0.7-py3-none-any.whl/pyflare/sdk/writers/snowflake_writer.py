import ast

from pyflare.sdk.config.write_config import WriteConfig
from pyflare.sdk.utils import pyflare_logger
from pyflare.sdk.writers.writer import Writer


class SnowflakeOutputWriter(Writer):

    SNOWFLAKE_WRITE_OPTIONS = '''{{
                "sfURL": "{connection_url}",
                "sfUser": "{connection_user}",
                "sfPassword": "{connection_password}",
                "sfDatabase": "{connection_database}",
                "sfSchema": "{collection}",
                "sfWarehouse": "{connection_warehouse}",
                "dbtable": "{dataset}"
            }}'''

    def __init__(self, write_config: WriteConfig):
        super().__init__(write_config)
        self.log = pyflare_logger.get_pyflare_logger(name=__name__)

    def write(self, df):
        # self.resolve_write_format()
        if self.write_config.is_stream:
            return self.write_stream()
        self.spark_options_conf()
        spark_options = self.write_config.spark_options
        # df = self.spark.sql(f"select * from {self.view_name}")
        df.write.options(**spark_options).format("snowflake").mode(self.write_config.mode).save()

    def write_stream(self):
        pass

    def spark_options_conf(self):
        snowflake_spark_option = ast.literal_eval(self.SNOWFLAKE_WRITE_OPTIONS.format(
            connection_url=self.write_config.depot_details.get('connection', {}).get('url', ""),
            connection_database=self.write_config.depot_details.get('connection', {}).get('database', ""),
            connection_warehouse=self.write_config.depot_details.get('connection', {}).get('warehouse', ""),
            connection_user=self.write_config.depot_details.get('secrets', {}).get('username', ""),
            connection_password=self.write_config.depot_details.get('secrets', {}).get('password', ""),
            collection=self.write_config.collection(),
            dataset=self.write_config.dataset_name()
        ))
        self.write_config.spark_options.update(snowflake_spark_option)

    def get_conf(self):
        return list()

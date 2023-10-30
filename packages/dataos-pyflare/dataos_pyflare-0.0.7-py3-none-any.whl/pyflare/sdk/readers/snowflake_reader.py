import ast

from pyflare.sdk.config.read_config import ReadConfig
from pyflare.sdk.readers.file_reader import Reader
from pyflare.sdk.utils import pyflare_logger, generic_utils


class SnowflakeInputReader(Reader):

    SNOWFLAKE_READ_OPTIONS = '''{{
            "sfURL": "{connection_url}",
            "sfUser": "{connection_user}",
            "sfPassword": "{connection_password}",
            "sfDatabase": "{connection_database}",
            "sfSchema": "{collection}",
            "sfWarehouse": "{connection_warehouse}",
            "dbtable": "{dataset}"
        }}'''

    def __init__(self, read_config: ReadConfig):
        super().__init__(read_config)
        self.log = pyflare_logger.get_pyflare_logger(name=__name__)

    def read(self):
        self.spark_options_conf()
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

    def spark_options_conf(self):
        snowflake_spark_option = ast.literal_eval(self.SNOWFLAKE_READ_OPTIONS.format(
            connection_url=self.read_config.depot_details.get('connection', {}).get('url', ""),
            connection_database=self.read_config.depot_details.get('connection', {}).get('database', ""),
            connection_warehouse=self.read_config.depot_details.get('connection', {}).get('warehouse', ""),
            connection_user=self.read_config.depot_details.get('secrets', {}).get('username', ""),
            connection_password=self.read_config.depot_details.get('secrets', {}).get('password', ""),
            collection=self.read_config.collection(),
            dataset=self.read_config.dataset_name()
        ))
        self.read_config.spark_options.update(snowflake_spark_option)

    def get_conf(self):
        return list()

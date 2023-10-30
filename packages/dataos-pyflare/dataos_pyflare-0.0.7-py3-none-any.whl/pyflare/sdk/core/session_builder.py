from __future__ import annotations

import logging
import re
from logging import Logger

from pyspark.conf import SparkConf
from pyspark.sql import SparkSession

from pyflare.sdk.config.constants import INPUT_STRING, OUTPUT_STRING, SPARK_APP_NAME, get_spark_app_name, \
    get_log4j_properties_path
from pyflare.sdk.utils import pyflare_logger
from pyflare.sdk.config import constants
from pyflare.sdk.config.read_config import ReadConfig
from pyflare.sdk.config.write_config import WriteConfig
from pyflare.sdk.depots import client

# DO NOT REMOVE IMPORTS, readers used at runtime
from pyflare.sdk.readers.reader import Reader
from pyflare.sdk.readers.file_reader import FileInputReader
from pyflare.sdk.readers.iceberg_reader import IcebergInputReader
from pyflare.sdk.readers.jdbc_reader import JDBCInputReader
from pyflare.sdk.readers.delta_reader import DeltaInputReader
from pyflare.sdk.readers.fastbase_reader import FastBaseInputReader
from pyflare.sdk.readers.snowflake_reader import SnowflakeInputReader
from pyflare.sdk.readers.bigquery_reader import BigqueryInputReader
from pyflare.sdk.readers.elasticsearch_reader import ElasticSearchInputReader

# DO NOT REMOVE IMPORTS, writers used at runtime
from pyflare.sdk.utils.generic_utils import resolve_dataos_address
from pyflare.sdk.utils.pyflare_exceptions import InvalidInputException
from pyflare.sdk.utils.pyflare_logger import create_log4j_on_disk
from pyflare.sdk.writers.writer import Writer
from pyflare.sdk.writers.file_writer import FileOutputWriter
from pyflare.sdk.writers.iceberg_writer import IcebergOutputWriter
from pyflare.sdk.writers.jdbc_writer import JDBCOutputWriter
from pyflare.sdk.writers.delta_writer import DeltaOutputWriter
from pyflare.sdk.writers.fastbase_writer import FastBaseOutputWriter
from pyflare.sdk.writers.snowflake_writer import SnowflakeOutputWriter
from pyflare.sdk.writers.bigquery_writer import BigqueryOutputWriter
from pyflare.sdk.writers.elasticsearch_writer import ElasticSearchOutputWriter

from pyflare.sdk.core.dataos_input import DataOSInput
from pyflare.sdk.core.minerva_input import MinervaInput
from pyflare.sdk.core.dataos_output import DataOSOutput

from urllib.parse import urlparse
from py4j.java_gateway import java_import
import os
from pyspark.sql import DataFrame

spark: SparkSession
g_inputs: dict
g_outputs: dict
g_dataos_token: str


class SparkSessionBuilder:
    spark: SparkSession = None
    spark_conf = list()
    parsed_inputs: dict = dict()
    parsed_outputs: dict = dict()
    api_token: str = ""
    dataos_fqdn: str = ""
    log_level: str = "INFO"
    logger: Logger = None

    def __init__(self, log_level: str):
        self.log_level = log_level
        self.logger = pyflare_logger.setup_pyflare_logger(self.log_level, name=__name__)
        create_log4j_on_disk(log_level)

    def build_session(self) -> SparkSession:
        if not self.spark:
            self.load_default_spark_conf()
            conf_obj = SparkConf().setAll(list(self.spark_conf))
            spark_builder = SparkSession.builder.config(conf=conf_obj)
            self.spark = spark_builder.getOrCreate()
        refresh_global_data(self)
        return self.spark

    def load_default_spark_conf(self) -> SparkSessionBuilder:
        self.spark_conf.insert(0,
                               ("spark.app.name", get_spark_app_name()))
        self.spark_conf.insert(0, ("spark.redaction.regex", "(?i)secret|password|key|abfss|dfs|apikey"))

        self.spark_conf.insert(0, ("spark.driverEnv.DATAOS_RUN_AS_APIKEY", self.api_token))
        self.spark_conf.insert(0, ("spark.heimdall.udf.provider",
                                   "io.dataos.flare.authz.DataOSSparkUdfProvider"))
        self.spark_conf.insert(0, ("spark.sql.extensions", "org.apache.iceberg.spark.extensions"
                                                           ".IcebergSparkSessionExtensions"))
        self.spark_conf.insert(0, (
            "spark.driver.extraJavaOptions", f"-Dlog4j.configuration=file:{get_log4j_properties_path()}")),
        self.spark_conf.insert(0, (
            "spark.executor.extraJavaOptions", f"-Dlog4j.configuration=file:{get_log4j_properties_path()}"))
        return self

    def with_spark_conf(self, conf) -> SparkSessionBuilder:
        self.spark_conf += conf
        app_name = [value for key, value in self.spark_conf if key == "spark.app.name"]
        os.environ[SPARK_APP_NAME] = app_name[0] if app_name else constants.SPARK_APP_NAME_PREFIX
        return self

    def with_readers(self, reader_address_list) -> SparkSessionBuilder:
        pass

    def with_writers(self, writer_address_list) -> SparkSessionBuilder:
        pass

    def with_depot(self, depot_name: str, acl: str = 'r') -> SparkSessionBuilder:
        ###
        # This code will be used if we support multi format read from same depot.
        # This has footprint in other classes, just blocking the entry point.
        ###
        # if format_list is None:
        #     format_list = [""]
        # if type(format_list) is not list:
        #     raise InvalidInputException("format_list cannot be empty, define list of formats to be used with_depot()")
        format_list = [""]
        if "rw" == acl.lower().strip():
            self.add_reader_instance(depot_name, format_list)
            self.add_writer_instance(depot_name, format_list)
        elif "r" == acl.lower().strip():
            self.add_reader_instance(depot_name, format_list)
        else:
            raise InvalidInputException("invalid value of acl, please assign an acceptable value ['r', 'rw']")
        return self

    def add_writer_instance(self, depot_name, format_list: list):
        for curr_format in format_list:
            writer_instance = self.__get_write_instance(depot_name=depot_name, write_format=curr_format)
            curr_format = writer_instance.write_config.io_format
            # writer_instance._view_name = f"{depot_name}_{curr_format}"  # to be used in case of multi format use case
            writer_instance._view_name = f"{depot_name}"
            self.parsed_outputs[writer_instance._view_name] = {"writer_instance": writer_instance}
            self.spark_conf += writer_instance.get_conf()

    def add_reader_instance(self, depot_name, format_list: list):
        for curr_format in format_list:
            reader_instance = self.__get_read_instance(depot_name=depot_name, read_format=curr_format)
            curr_format = reader_instance.read_config.io_format
            # reader_instance._view_name = f"{depot_name}_{curr_format}"  # to be used in case of multi format use case
            reader_instance._view_name = f"{depot_name}"
            self.parsed_inputs[reader_instance._view_name] = {"reader_instance": reader_instance}
            self.spark_conf += reader_instance.get_conf()

    def with_user_apikey(self, apikey: str):
        self.api_token = apikey
        return self

    def with_dataos_fqdn(self, dataos_fqdn: str):
        self.dataos_fqdn = dataos_fqdn
        constants.DATAOS_BASE_URL = dataos_fqdn
        return self

    def __get_read_instance(self, depot_name: str, read_format: str) -> Reader:
        if self.__is_local(depot_name):
            depot_details = {"type": "local", "connection": {"localUrl": f"{depot_name}"}}
        else:
            depot_details = client.DepotClientAPI(self.api_token).get_depot_details(depot_name)
        if read_format:
            depot_details["format"] = read_format
        conf_obj = ReadConfig(depot_details=depot_details)
        return self.__create_input_instance("Reader", conf_obj)

    def __get_write_instance(self, depot_name: str, write_format: str) -> Writer:
        depot_details = client.DepotClientAPI(self.api_token).get_depot_details(depot_name)
        if write_format:
            depot_details["format"] = write_format
        conf_obj = WriteConfig(depot_details=depot_details)
        return self.__create_output_instance("Writer", conf_obj)

    def __create_input_instance(self, class_suffix: str, conf_obj: ReadConfig) -> Reader:
        io_format = conf_obj.io_format.casefold()
        self.logger.debug(f"input_format: {io_format}")
        if io_format in ["pulsar"]:
            return globals()[f"FastBase{INPUT_STRING}{class_suffix}"](conf_obj)
        if io_format in ["delta", "deltabase"]:
            return globals()[f"Delta{INPUT_STRING}{class_suffix}"](conf_obj)
        if io_format in ("postgresql", "postgres", "jdbc", "mysql", "oracle", "redshift"):
            return globals()[f"JDBC{INPUT_STRING}{class_suffix}"](conf_obj)
        elif io_format == "iceberg":
            return globals()[f"Iceberg{INPUT_STRING}{class_suffix}"](conf_obj)
        elif io_format == "snowflake":
            return globals()[f"Snowflake{INPUT_STRING}{class_suffix}"](conf_obj)
        elif io_format == "bigquery":
            return globals()[f"Bigquery{INPUT_STRING}{class_suffix}"](conf_obj)
        elif io_format == "elasticsearch":
            return globals()[f"ElasticSearch{INPUT_STRING}{class_suffix}"](conf_obj)
        else:
            return globals()[f"File{INPUT_STRING}{class_suffix}"](conf_obj)

    def __create_output_instance(self, class_suffix: str, conf_obj: WriteConfig) -> Writer:
        io_format = conf_obj.io_format.casefold()
        self.logger.debug(f"output_format: {io_format}")
        if io_format in ["pulsar"]:
            return globals()[f"FastBase{OUTPUT_STRING}{class_suffix}"](conf_obj)
        if io_format in ["delta", "deltabase"]:
            return globals()[f"Delta{OUTPUT_STRING}{class_suffix}"](conf_obj)
        if io_format in ("postgresql", "postgres", "jdbc", "mysql", "oracle", "redshift"):
            return globals()[f"JDBC{OUTPUT_STRING}{class_suffix}"](conf_obj)
        elif io_format == "iceberg":
            return globals()[f"Iceberg{OUTPUT_STRING}{class_suffix}"](conf_obj)
        elif io_format == "snowflake":
            return globals()[f"Snowflake{OUTPUT_STRING}{class_suffix}"](conf_obj)
        elif io_format == "bigquery":
            return globals()[f"Bigquery{OUTPUT_STRING}{class_suffix}"](conf_obj)
        elif io_format == "elasticsearch":
            return globals()[f"ElasticSearch{OUTPUT_STRING}{class_suffix}"](conf_obj)
        else:
            return globals()[f"FileOutput{class_suffix}"](conf_obj)

    def __is_local(self, path):
        if os.path.exists(path):
            return True
        # elif urlparse(path).scheme in ['', 'file']:
        #     return True
        return False


def refresh_global_data(spark_session_builder: SparkSessionBuilder):
    global g_inputs, g_outputs, spark, g_dataos_token
    g_inputs = spark_session_builder.parsed_inputs
    g_outputs = spark_session_builder.parsed_outputs
    g_dataos_token = spark_session_builder.api_token

    spark = spark_session_builder.spark
    # pyflare_logger.update_spark_log_level(spark, spark_session_builder.log_level)


def load(name, format, driver=None, query=None, options=None):
    """

        Read dataset from the source with the supplied parameters.

        Args:
            name (str): Name of input key to read
            format (str): Read format
            optional params -
            driver (str): driver to read source
            query (str): Query to be executed
            options (dict): Spark and other supported properties to be used during read

        Example:
            ------------- Icebase --------------
            read_options = {
                'compression': 'gzip',
                'iceberg': {
                    'table_properties': {
                        'read.split.target-size': 134217728,
                        "read.split.metadata-target-size": 33554432
                        }
                }
            }

            @dataos_source(name="ct", source_format="iceberg", options=read_options)

            ------------- JDBC --------------
            read_options = {
                'compression': 'gzip',
                "partitionColumn": "last_update",
                "lowerBound": datetime.datetime(2008,1,1),
                "upperBound": datetime.datetime(2009,1,1),
                "numPartitions": 6
                }

            @dataos_source(name="ct", source_format="postgresql", driver="com.mysql.cj.jdbc.Driver", options=read_options)
            Supported JDBC sub-protocols:
                * postgresql: org.postgresql.Driver
                * mysql: com.mysql.cj.jdbc.Driver

    """
    global g_inputs, spark, g_dataos_token
    java_import(spark._jvm, "io.dataos.spark.authz.util.DataGovernor")
    java_import(spark._jvm, "io.dataos.spark.authz.util.DataPolicyClient")
    java_import(spark._jvm, "io.dataos.datapolicy.model.DepotCollectionDataset")
    # to-do parse depot name form  depot address
    os_input = DataOSInput(name=name, parsed_inputs=g_inputs, spark=spark,
                           source_format=format,
                           driver=driver, query=query, options=options)
    source_df, depot_name = os_input.process_inputs()
    depot_details = os_input.parsed_inputs[depot_name]['reader_instance'].read_config.depot_details
    dataset_address = ".".join([depot_details.get("depot", ""), depot_details.get("collection", ""),
                                depot_details.get("dataset", "")])
    dp_client = spark._jvm.DataPolicyClient.getInstance(os.environ.get("GATEWAY_BASE_URL", ""), g_dataos_token)
    data_govern_jvm = spark._jvm.DataGovernor.getInstance(dp_client)
    governed_data = data_govern_jvm.govern(dataset_address, source_df._jdf)
    governed_df = source_df
    if governed_data._1().isDefined():
        # here we are extracting first element of tuple we got from govern() response and converting java datafrme to
        # python df
        governed_df = DataFrame(governed_data._1().get(), spark)
    return governed_df


def minerva_input(name, query, driver="io.trino.jdbc.TrinoDriver", options=None):
    """

        Read dataset from the source with the supplied parameters.

        Args:
            name (str): Name of input key to read
            query (str): Query to be executed

            optional params -
            driver (str): driver needed to read source. Default driver is jdbc.TrinoDriver.
            options (dict): Spark and other supported properties to be used during read.

        Example:
            read_options = { "source": "pyflare.sdk/0.0.20.0" }
            query = "SELECT city_id, city_name, cast(ts_city AS varchar) "ts_city FROM icebase.retail.city"
            @minerva_input(name="ice", query=q2, options=read_options)
    """
    global g_inputs, spark
    minerva_in = MinervaInput(name=name, parsed_inputs=g_inputs, spark=spark, driver=driver, query=query,
                              options=options)
    minerva_df = minerva_in.process_inputs()
    return minerva_df


def save(name: str, dataframe, format: str = None, mode="append", driver=None, options=None):
    """
        Write the transformed dataset to sink, with the supplied parameters.

        Args:
            name (str): Name of output key to write
            format (str): Write format
            mode (str): Write format, default value "append"
            driver (str): driver need to read source
            options (dict): Spark and other supported properties to be used during write

        Example:
            write_options = {
                "compression": "gzip",
                "iceberg": {
                    "table_properties": {
                        "write.format.default": "parquet",
                        "write.parquet.compression-codec": "gzip",
                        "write.metadata.previous-versions-max": 3,
                        "parquet.page.write-checksum.enabled": "false"
                    },
                    "partition": [
                        {
                            "type": "months",
                            "column": "ts_city"
                        },
                        {
                            "type": "bucket",
                            "column": "city_id",
                            "bucket_count": 8
                        },
                        {
                            "type": "identity",
                            "column": "city_name"
                        }
                    ]
                }
            }

            @dataos_sink(name="c360", sink_format="iceberg", mode="append", options=write_options)
            :param dataframe:

        """
    global g_outputs, spark
    # to-do parse depot name form  depot address
    DataOSOutput(name=name, dataframe=dataframe, parsed_outputs=g_outputs, spark=spark, sink_format=format, mode=mode,
                 driver=driver, options=options)

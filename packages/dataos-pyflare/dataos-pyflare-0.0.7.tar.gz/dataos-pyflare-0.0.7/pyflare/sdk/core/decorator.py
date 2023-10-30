# from pyflare.sdk import logger
# from pyflare.sdk.config import constants
# from pyflare.sdk.core.dataos_input import DataOSInput
# from pyflare.sdk.core.minerva_input import MinervaInput
# from pyflare.sdk.core.dataos_output import DataOSOutput
# from pyflare.sdk.core.session_builder import SparkSessionBuilder
# from pyspark.sql import SparkSession
#
#
# log = logger.get(__name__)
#
# spark: SparkSession
# g_inputs: dict
# g_outputs: dict
# g_dataos_token: str
#
#
# def refresh_global_data(spark_session_builder: SparkSessionBuilder):
#     global g_inputs, g_outputs, spark, g_dataos_token
#     constants.DATAOS_BASE_URL = spark_session_builder.dataos_fqdn
#     logger.set_spark_log_level(spark, log.getEffectiveLevel())
#     g_inputs = spark_session_builder.parsed_inputs
#     g_outputs = spark_session_builder.parsed_outputs
#     log.debug(f"Parsed_inputs: {g_inputs}, Parsed_outputs: {g_outputs}")
#     spark = spark_session_builder.build_session()
#
#
# # def session(api_key: str, dataos_url: str, inputs: dict = None, outputs: dict = None,
# #             spark_conf_options: list = None) -> SparkSession:
# #     """
# #
# #     Creates spark session from supplied parameters.
# #
# #     Args:
# #         api_key (str): Dataos auth token.
# #         dataos_url (str): Fully qualified domain name of Dataos.
# #         inputs (dict): Dictionary of inputs to be read.
# #         optional params -
# #         outputs (dict): Dictionary of outputs to be written.
# #         spark_conf_options (list): Custom spark conf you want to supply to spark session.
# #
# #     Returns:
# #         object: SparkSession
# #
# #     Example:
# #
# #         inputs = { "ct1": "dataos://icebase:retail/city1",
# #                     "ct2": "dataos://icebase:retail/city2"
# #                 }
# #
# #         outputs =
# #         {
# #             "c360": "dataos://icebase:outputs/c360_00_1"
# #         }
# #
# #         sparkConf = [
# #             ("spark.app.name", "Dataos Sdk Spark App"),
# #             ("spark.master", "local[*]"),
# #             ("spark.jars.packages", "org.apache.iceberg:iceberg-spark3:0.13.2,org.apache.spark:spark-sql_2.12:3.3.0,"
# #                                     "com.microsoft.azure:azure-storage:8.6.6,org.apache.hadoop:hadoop-azure:3.3.3")
# #         ]
# #
# #         DATAOS_FQDN = "main-lamb.dataos.app"
# #
# #         token = "dGVzdF90b2tlbi40MjJmZTQ4Zi04ZWU4LTRjZTQtODczNS0zNGI5N2ZkZTIwODg="
# #
# #         spark = session(api_key=token, dataos_url=DATAOS_FQDN, inputs=inputs, outputs=outputs,
# #                     spark_conf_options=sparkConf)
# #     """
# #     global g_inputs, g_outputs, spark, g_dataos_token
# #     constants.DATAOS_BASE_URL = dataos_url
# #     g_inputs = inputs if inputs else {}
# #     g_outputs = outputs if outputs else {}
# #     g_dataos_token = api_key
# #     spark_conf_options = spark_conf_options if spark_conf_options else []
# #     spark_session_builder = session_builder.SparkSessionBuilder(g_dataos_token).load_input_conf(
# #         g_inputs).load_output_conf(g_outputs).load_default_spark_conf(spark_conf_options)
# #     spark = spark_session_builder.build_session()
# #     logger.set_spark_log_level(spark, log.getEffectiveLevel())
# #     g_inputs = spark_session_builder.parsed_inputs
# #     g_outputs = spark_session_builder.parsed_outputs
# #     log.debug(f"Parsed_inputs: {g_inputs}, Parsed_outputs: {g_outputs}")
# #     return spark
#
#
# def load(name, format=None, driver=None, query=None, options=None):
#     """
#
#         Read dataset from the source with the supplied parameters.
#
#         Args:
#             name (str): Name of input key to read
#             optional params -
#             format (str): Read format
#             driver (str): driver need to read source
#             query (str): Query to be executed
#             options (dict): Spark and other supported properties to be used during read
#
#         Example:
#             ------------- Icebase --------------
#             read_options = {
#                 'compression': 'gzip',
#                 'iceberg': {
#                     'table_properties': {
#                         'read.split.target-size': 134217728,
#                         "read.split.metadata-target-size": 33554432
#                         }
#                 }
#             }
#
#             @dataos_source(name="ct", source_format="iceberg", options=read_options)
#
#             ------------- JDBC --------------
#             read_options = {
#                 'compression': 'gzip',
#                 "partitionColumn": "last_update",
#                 "lowerBound": datetime.datetime(2008,1,1),
#                 "upperBound": datetime.datetime(2009,1,1),
#                 "numPartitions": 6
#                 }
#
#             @dataos_source(name="ct", source_format="postgresql", driver="com.mysql.cj.jdbc.Driver", options=read_options)
#             Supported JDBC sub-protocols:
#                 * postgresql: org.postgresql.Driver
#                 * mysql: com.mysql.cj.jdbc.Driver
#
#     """
#     global g_inputs, spark
#     # to-do parse depot name form  depot address
#     os_input = DataOSInput(name=name, parsed_inputs=g_inputs, spark=spark, source_format=format,
#                            driver=driver, query=query, options=options)
#     source_df = os_input.process_inputs()
#     return source_df
#
#
# def minerva_input(name, query, driver="io.trino.jdbc.TrinoDriver", options=None):
#     """
#
#         Read dataset from the source with the supplied parameters.
#
#         Args:
#             name (str): Name of input key to read
#             query (str): Query to be executed
#
#             optional params -
#             driver (str): driver needed to read source. Default driver is jdbc.TrinoDriver.
#             options (dict): Spark and other supported properties to be used during read.
#
#         Example:
#             read_options = { "source": "pyflare.sdk/0.0.20.0" }
#             query = "SELECT city_id, city_name, cast(ts_city AS varchar) "ts_city FROM icebase.retail.city"
#             @minerva_input(name="ice", query=q2, options=read_options)
#     """
#     global g_inputs, spark
#     minerva_in = MinervaInput(name=name, parsed_inputs=g_inputs, spark=spark, driver=driver, query=query,
#                               options=options)
#     minerva_df = minerva_in.process_inputs()
#     return minerva_df
#
#
# def save(name: str, format: str = None, mode="append", driver=None, options=None):
#     """
#         Write the transformed dataset to sink, with the supplied parameters.
#
#         Args:
#             name (str): Name of output key to write
#             format (str): Write format
#             mode (str): Write format, default value "append"
#             driver (str): driver need to read source
#             options (dict): Spark and other supported properties to be used during write
#
#         Example:
#             write_options = {
#                 "compression": "gzip",
#                 "iceberg": {
#                     "table_properties": {
#                         "write.format.default": "parquet",
#                         "write.parquet.compression-codec": "gzip",
#                         "write.metadata.previous-versions-max": 3,
#                         "parquet.page.write-checksum.enabled": "false"
#                     },
#                     "partition": [
#                         {
#                             "type": "months",
#                             "column": "ts_city"
#                         },
#                         {
#                             "type": "bucket",
#                             "column": "city_id",
#                             "bucket_count": 8
#                         },
#                         {
#                             "type": "identity",
#                             "column": "city_name"
#                         }
#                     ]
#                 }
#             }
#
#             @dataos_sink(name="c360", sink_format="iceberg", mode="append", options=write_options)
#
#         """
#     global g_outputs, spark
#     # to-do parse depot name form  depot address
#     DataOSOutput(name=name, parsed_outputs=g_outputs, spark=spark, sink_format=format, mode=mode,
#                  driver=driver, options=options)

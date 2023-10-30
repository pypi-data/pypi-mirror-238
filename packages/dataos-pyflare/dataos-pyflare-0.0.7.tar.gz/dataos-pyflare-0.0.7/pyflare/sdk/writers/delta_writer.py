import ast
import base64
import time

import pyspark.sql.functions as F
from pyflare.sdk.config import constants
from pyflare.sdk.config.write_config import WriteConfig
from pyflare.sdk.utils import pyflare_logger, generic_utils
from pyflare.sdk.writers.file_writer import FileOutputWriter
from pyspark.sql.readwriter import DataFrameWriter


class DeltaOutputWriter(FileOutputWriter):
    DELTA_CONF = '''[
            ("spark.sql.catalog.spark_catalog","org.apache.spark.sql.delta.catalog.DeltaCatalog"),
            ("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        ]'''

    def __init__(self, write_config: WriteConfig):
        super().__init__(write_config)
        self.log = pyflare_logger.get_pyflare_logger(name=__name__)

    def write(self, df):
        if "merge" in self.write_config.extra_options.keys():
            """
            ToDo - Explore Catalog configuration for delta lake storage
            Right now it is forcing to hardcode spark_catalog key for above spark 
            conf.
            # depot = self.write_config.depot_details.get("depot")
            # collection = self.write_config.depot_details.get("collection")
            # dataset = self.write_config.depot_details.get("dataset")
            # view_name = f"{depot}_{collection}_{dataset}_{int(time.time() * 1e9)}"
            #
            # df.createOrReplaceTempView(view_name)
            # self.spark.sql(self.__merge_into_query(view_name, depot, collection, dataset))
            """
            pass
        else:
            spark_options = self.write_config.spark_options
            io_format = self.write_config.io_format
            dataset_path = self.write_config.dataset_absolute_path()
            # df = self.spark.sql(f"select * from {self.view_name}")
            df_writer = df.write.format(io_format)
            if spark_options:
                df_writer = df_writer.options(**spark_options)
            self.log.info(f"spark options: {spark_options}")
            df_writer = self.__process_partition_conf(df_writer)
            df_writer.mode(self.write_config.mode).save(dataset_path)

    def write_stream(self):
        pass

    def get_conf(self):
        # print("calling write -> :", f"_{self.write_config.depot_type()}_{self.write_config.io_format}")
        return getattr(self, f"_{self.write_config.depot_type()}_{self.write_config.io_format}")()

    def _abfss_delta(self):
        delta_conf = ast.literal_eval(self.DELTA_CONF)
        delta_conf.extend(generic_utils.get_abfss_spark_conf(self.write_config))
        return delta_conf

    def __process_partition_conf(self, df_writer):
        partition_columns = []
        for temp_dict in self.write_config.extra_options.get("partition", []):
            partition_columns.append(temp_dict.get("column", ''))
        if partition_columns:
            self.log.info(f"partition column: {partition_columns}")
            df_writer = df_writer.partitionBy(partition_columns)
        return df_writer

    # def __merge_into_query(self, source_view: str, depot, collection, dataset):
    #     merge_clauses = self.write_config.extra_options.get("merge", {})
    #
    #     query = f"MERGE INTO spark_catalog.{collection}.{dataset} as target \n"
    #     query += f"USING (select * from {source_view}) as source \n"
    #     query += f"ON {merge_clauses.get('onClause', '')} \n"
    #     query += f"{merge_clauses.get('whenClause', '')} \n"
    #     return query

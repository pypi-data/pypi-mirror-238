import ast
import base64
import time
import warnings
import pyspark.sql.functions as F
from pyflare.sdk.config import constants
from pyflare.sdk.config.constants import S3_ICEBERG_FILE_IO
from pyflare.sdk.config.write_config import WriteConfig
from pyflare.sdk.utils import pyflare_logger, generic_utils
from pyflare.sdk.writers.file_writer import FileOutputWriter
from pyspark.sql.readwriter import DataFrameWriterV2

warnings.filterwarnings("ignore", message=".*version-hint.text.*")


class IcebergOutputWriter(FileOutputWriter):
    ICEBERG_CONF = '''[
            ("spark.sql.catalog.{catalog_name}", "org.apache.iceberg.spark.SparkCatalog"),
            ("spark.sql.catalog.{catalog_name}.type", "hadoop"),
            ("spark.sql.catalog.{catalog_name}.warehouse", "{depot_base_path}")
        ]'''

    def __init__(self, write_config: WriteConfig):
        super().__init__(write_config)
        self.log = pyflare_logger.get_pyflare_logger(name=__name__)

    def write(self, df):
        if "merge" in self.write_config.extra_options.keys():
            depot = self.write_config.depot_details.get("depot")
            collection = self.write_config.depot_details.get("collection")
            dataset = self.write_config.depot_details.get("dataset")
            view_name = f"{depot}_{collection}_{dataset}_{int(time.time() * 1e9)}"

            df.createOrReplaceTempView(view_name)
            self.spark.sql(self.__merge_into_query(view_name, depot, collection, dataset))
        else:
            spark_options = self.write_config.spark_options
            table_properties = self.write_config.extra_options.get("table_properties", {})
            io_format = self.write_config.io_format
            dataset_path = generic_utils.get_dataset_path(self.write_config)
            # df = self.spark.sql(f"select * from {self.view_name}")
            df_writer = df.writeTo(dataset_path).using(io_format)
            if spark_options:
                df_writer = df_writer.options(**spark_options)
            self.log.info(f"spark options: {spark_options}")
            if table_properties:
                self.log.info(f"table_properties: {table_properties}")
                df_writer = df_writer.tableProperty(**table_properties)
            df_writer = self.__process_partition_conf(df_writer)
            self.__write_mode(df_writer)

    def write_stream(self):
        pass

    def get_conf(self):
        return getattr(self, f"_{self.write_config.depot_type()}_{self.write_config.io_format}")()

    def _abfss_iceberg(self):
        dataset_absolute_path = self.write_config.dataset_absolute_path()
        # depot_base_path = dataset_absolute_path.split(self.write_config.collection())[0]
        iceberg_conf = ast.literal_eval(self.ICEBERG_CONF.format(catalog_name=self.write_config.depot_name(),
                                                                 depot_base_path=dataset_absolute_path))
        iceberg_conf.extend(generic_utils.get_abfss_spark_conf(self.write_config))
        return iceberg_conf

    def _s3_iceberg(self):
        dataset_absolute_path = self.write_config.dataset_absolute_path()
        # depot_base_path = dataset_absolute_path.split(self.write_config.collection())[0]
        iceberg_conf = ast.literal_eval(self.ICEBERG_CONF.format(catalog_name=self.write_config.depot_name(),
                                                                 depot_base_path=dataset_absolute_path))
        iceberg_conf.append(S3_ICEBERG_FILE_IO)
        iceberg_conf.extend(generic_utils.get_s3_spark_conf(self.write_config))
        return iceberg_conf

    def _gcs_iceberg(self):
        dataset_absolute_path = self.write_config.dataset_absolute_path()
        # depot_base_path = dataset_absolute_path.split(self.write_config.collection())[0]
        iceberg_conf = ast.literal_eval(self.ICEBERG_CONF.format(catalog_name=self.write_config.depot_name(),
                                                                 depot_base_path=dataset_absolute_path))
        iceberg_conf.extend(generic_utils.get_gcs_spark_conf(self.write_config))
        return iceberg_conf

    def __process_partition_conf(self, df_writer: DataFrameWriterV2) -> DataFrameWriterV2:
        partition_column_list = []
        for temp_dict in self.write_config.extra_options.get("partition", []):
            partition_scheme: str = temp_dict.get("type", "")
            partition_column: str = temp_dict.get("column", "")
            if partition_scheme.casefold() in ["year", "month", "day", "hour"]:
                self.log.info(f"partition scheme: {partition_scheme}, partition column: {partition_column}")
                partition_column_list.append(getattr(F, f"{partition_scheme}s")(partition_column))
            elif partition_scheme.casefold() == "bucket":
                bucket_count: int = temp_dict.get("bucket_count", 8)
                self.log.info(
                    f"partition scheme: {partition_scheme}, partition column: {partition_column}, "
                    f"bucket_count: {bucket_count}")
                self.log.info(f"F.bucket({bucket_count}, {partition_column}")
                partition_column_list.append(getattr(F, f"{partition_scheme}")(bucket_count, F.col(partition_column)))
            elif partition_scheme.casefold() == "identity":
                self.log.info(f"partition column: {partition_column}")
                partition_column_list.append(F.col(partition_column))
            else:
                self.log.warn(f"Invalid partition scheme: {partition_scheme}")
        if partition_column_list:
            df_writer = df_writer.partitionedBy(*partition_column_list)
        return df_writer

    def __write_mode(self, df: DataFrameWriterV2):
        if self.write_config.mode in ["create", "overwrite", "write"]:
            df.createOrReplace()
        elif self.write_config.mode in ['overwriteByPartition']:
            df.overwritePartitions()
        else:
            df.append()

    def __merge_into_query(self, source_view: str, depot, collection, dataset):
        merge_clauses = self.write_config.extra_options.get("merge", {})

        query = f"MERGE INTO {depot}.{collection}.{dataset} as target \n"
        query += f"USING (select * from {source_view}) as source \n"
        query += f"ON {merge_clauses.get('onClause', '')} \n"
        query += f"{merge_clauses.get('whenClause', '')} \n"
        return query

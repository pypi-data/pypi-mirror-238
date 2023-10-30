# from __future__ import annotations
from pyflare.sdk import pyflare_logger
from pyflare.sdk.readers.minerva_reader import MinervaInputReader
from pyflare.sdk.readers.reader import Reader
from pyflare.sdk.utils.generic_utils import safe_assignment
from pyspark.sql import SparkSession, DataFrame


class MinervaInput:
    def __init__(self, name, parsed_inputs, spark,
                 source_format="jdbc", driver="io.trino.jdbc.TrinoDriver", query=None, options=None):
        self.input_name: str = name
        self.parsed_inputs: dict[str: Reader] = parsed_inputs
        self.spark: SparkSession = spark
        self.source_format: str = source_format
        self.driver = driver
        self.query = query
        self.options: dict = options if options else {}
    
    def process_inputs(self) -> DataFrame:
        """

        Run query on minerva and the result is stored as a temp view
        with the name passed in the dataos_source decorator.
        """
        log = pyflare_logger.get_pyflare_logger(name=__name__)
        log.debug(f"minerva_read_input, input: {self.parsed_inputs}")
        log.debug(self.parsed_inputs)
        reader_instance: Reader = self.parsed_inputs.get(self.input_name).get('reader_instance')
        minerva_reader: MinervaInputReader = MinervaInputReader(reader_instance.read_config)
        minerva_reader.read_config.driver = self.driver
        minerva_reader.read_config.query = self.query
        minerva_reader.spark = safe_assignment(minerva_reader.spark, self.spark)
        minerva_reader.read_config.io_format = safe_assignment(minerva_reader.read_config.io_format,
                                                               self.source_format)
        minerva_reader.read_config.extra_options = safe_assignment(minerva_reader.read_config.extra_options,
                                                                   self.options.pop(
                                                                       minerva_reader.read_config.io_format, {}))
        minerva_reader.read_config.spark_options = safe_assignment(minerva_reader.read_config.spark_options,
                                                                   self.options)
        df = minerva_reader.read()
        # df.createOrReplaceTempView(self.input_name)
        return df

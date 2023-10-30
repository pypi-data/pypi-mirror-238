from pyflare.sdk import pyflare_logger
from pyflare.sdk.utils.generic_utils import safe_assignment, append_properties, resolve_dataos_address
from pyflare.sdk.writers.writer import Writer
from pyspark.sql import SparkSession


class DataOSOutput:
    def __init__(self, name, dataframe, parsed_outputs, spark, is_stream=None,
                 sink_format=None, mode=None, driver=None, options=None):
        self.output_name: str = name
        self.parsed_outputs: dict[str: Writer] = parsed_outputs
        self.spark: SparkSession = spark
        self.is_stream: bool = is_stream
        self.mode: str = mode
        self.driver = driver
        self.options: dict = options if options else {}
        self.sink_format: str = sink_format
        self.dataframe = dataframe
        self.process_outputs()

    def process_outputs(self):
        """

        Write the transformed dataset to sink, with the supplied parameters to dataos_sink decorator.
        """
        log = pyflare_logger.get_pyflare_logger(name=__name__)
        log.debug(f"dataos_write_output, output: {self.parsed_outputs}")
        resolved_address = resolve_dataos_address(self.output_name)
        writer_instance: Writer = self.parsed_outputs.get(resolved_address.get("depot", "")).get('writer_instance')
        writer_instance.write_config.depot_details["collection"] = resolved_address.get("collection", "")
        writer_instance.write_config.depot_details["dataset"] = resolved_address.get("dataset", "")
        writer_instance.write_config.driver = self.driver
        writer_instance.spark = safe_assignment(writer_instance.spark, self.spark)
        # writer_instance.write_config.io_format = safe_assignment(writer_instance.write_config.io_format,
        #                                                          self.sink_format)
        writer_instance.write_config.mode = safe_assignment(writer_instance.write_config.mode, self.mode)
        writer_instance.write_config.extra_options = append_properties(writer_instance.write_config.extra_options,
                                                                       self.options.pop(
                                                                           writer_instance.write_config.io_format,
                                                                           {}))
        writer_instance.write_config.spark_options = append_properties(writer_instance.write_config.spark_options,
                                                                       self.options)
        writer_instance.write(self.dataframe)

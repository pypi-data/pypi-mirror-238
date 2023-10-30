import abc

from pyflare.sdk.config.write_config import WriteConfig
from pyspark.sql import SparkSession


class Writer(metaclass=abc.ABCMeta):
    
    def __init__(self, write_config: WriteConfig):
        self._write_config = write_config
        self._spark: SparkSession = None
        self._view_name: str = ""
    
    @abc.abstractmethod
    def write(self, df):
        pass
    
    @abc.abstractmethod
    def write_stream(self):
        pass
    
    @abc.abstractmethod
    def get_conf(self):
        pass
    
    @property
    def spark(self) -> SparkSession:
        return self._spark
    
    @spark.setter
    def spark(self, value):
        self._spark = value
    
    @property
    def view_name(self):
        return self._view_name
    
    @view_name.setter
    def view_name(self, value):
        self._view_name = value
    
    @property
    def write_config(self) -> WriteConfig:
        return self._write_config
    
    @write_config.setter
    def write_config(self, value):
        self._write_config = value

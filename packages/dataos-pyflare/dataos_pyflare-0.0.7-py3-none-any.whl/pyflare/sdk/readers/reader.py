import abc

from pyspark.sql import SparkSession

from pyflare.sdk.config.read_config import ReadConfig


class Reader(metaclass=abc.ABCMeta):
    
    def __init__(self, read_config: ReadConfig):
        self._spark: SparkSession = None
        self._view_name: str = ""
        self._read_config = read_config
    
    @abc.abstractmethod
    def read(self):
        pass
    
    @abc.abstractmethod
    def read_stream(self):
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
    def view_name(self) -> str:
        return self._view_name
    
    @view_name.setter
    def view_name(self, value):
        self._view_name = value
    
    @property
    def read_config(self) -> ReadConfig:
        return self._read_config
    
    @read_config.setter
    def read_config(self, value):
        self._read_config = value

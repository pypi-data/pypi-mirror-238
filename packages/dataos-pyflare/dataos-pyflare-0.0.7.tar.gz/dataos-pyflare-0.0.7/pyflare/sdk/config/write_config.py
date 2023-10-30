class WriteConfig:
    
    def __init__(self, depot_details: dict):
        self._depot_details = depot_details
        self._io_format = self.format_resolver()
        self._is_stream = False
        self._mode = "append"
        self._driver = ""
        self._spark_options: dict = {}
        self._extra_options: dict = {}
    
    def depot_name(self) -> str:
        """
        Returns depot name
        """
        return self._depot_details.get("depot", "")
    
    def depot_type(self) -> str:
        """
        Returns depot type
        """
        return self._depot_details.get("type", "")
    
    def collection(self) -> str:
        """
        Returns depot collection name
        """
        return self._depot_details.get("collection", "")
    
    def dataset_name(self) -> str:
        """
        Returns depot dataset name
        """
        return self._depot_details.get("dataset", "")

    def dataset_absolute_path(self) -> str:
        """
        Returns an absolute path of dataset
        """
        return self._depot_details.get("connection", {}).get(f"{self.depot_type()}Url", )

    def connection(self) -> dict:
        """
        Returns connection dict
        """
        return self._depot_details.get("connection", {})

    @property
    def io_format(self):
        return self._io_format

    @property
    def depot_details(self):
        return self._depot_details

    @property
    def is_stream(self):
        return self._is_stream
    
    @property
    def mode(self) -> str:
        return self._mode

    @property
    def driver(self):
        return self._driver
    
    @property
    def spark_options(self):
        return self._spark_options
    
    @property
    def extra_options(self):
        return self._extra_options
    
    @io_format.setter
    def io_format(self, value):
        self._io_format = value
    
    @depot_details.setter
    def depot_details(self, value):
        self._depot_details = value
    
    @is_stream.setter
    def is_stream(self, value):
        self._is_stream = value
    
    @mode.setter
    def mode(self, value):
        self._mode = value

    @driver.setter
    def driver(self, value):
        self._driver = value
    
    @spark_options.setter
    def spark_options(self, value):
        self._spark_options = value
    
    @extra_options.setter
    def extra_options(self, value):
        self._extra_options = value

    def format_resolver(self):
        io_format = self.depot_details.get("format", "")
        sub_protocol = self.connection().get("subprotocol", "")
        if not io_format:
            io_format = self.depot_type()
        if sub_protocol:
            io_format = sub_protocol
        return io_format

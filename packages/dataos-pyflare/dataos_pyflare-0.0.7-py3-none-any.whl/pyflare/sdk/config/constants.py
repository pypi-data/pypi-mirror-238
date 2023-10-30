import os

SPARK_APP_NAME_PREFIX = "DataOS Pyflare"
SPARK_APP_NAME = "SPARK_APP_NAME"
HTTP_PROTOCOL = "https"
DATAOS_BASE_URL = ""
HTTPS_PREFIX = "https://"

DEPOT_METADATA_ENDPOINT = "{}://{}/ds/api/v2/depots/{}"
DEPOT_RESOLVE_ENDPOINT = "{}://{}/ds/api/v2/resolve?address={}"
DEPOT_RESOLVE_ENDPOINT_CUSTOM = "{}://{}/ds/api/v2/resolve?address=dataos://{}"
DEPOT_SECRETS_ENDPOINT = f"{DEPOT_METADATA_ENDPOINT}/secrets"
DEPOT_METADETA_HEADER_KEY = "Apikey"
TYPE = "type"
NAME = "name"
FORMAT = "format"
HTTP_GET = "GET"
DATAOS_ADDRESS_RESOLVER_REGEX = "dataos:\\/\\/([a-zA-Z0-9-]+)(:([a-zA-Z0-9_]+))(\\/(.*))*"
UTF8 = "utf-8"
BASE64VALUE = "base64Value"
CONTAINER = "container"
ACCOUNT = "account"
ENDPOINT_SUFFIX = "endpointSuffix"
CATALOG = "catalog"
STORAGE_ACCOUNT_KEY = "storageaccountkey"
STORAGE_ACCOUNT_NAME = "storageaccountname"
AZURE_ACCOUNT_KEY = "azurestorageaccountkey"
ICEBASE = "icebase"
AZURE_ACCOUNT_KEY_PREFIX = "fs.azure.account.key"
FILE_PROTOCOL_TYPE = "file_protocol_type"
DATASET_FORMAT = "dataset_format"
DATASET_LOCATION = "dataset_location"
ABFSS = "abfss"
WASBS = "wasbs"
PULSAR = "pulsar"
RELATIVE_PATH = "relativePath"
PASSWORD = "password"
USERNAME = "username"
MINEVRA_URL = "jdbc:trino://tcp.{}:7432"
OUTPUT_STRING = "Output"
INPUT_STRING = "Input"
DEPOT_NAME_JSON_FILE_REGEX = r'^{depot_name}_.*\.json$'
DEPOT_SECRETS_KV_REGEX = r"(\w+)=(.*?)\n[ \t]*"
DATAOS_DEFAULT_SECRET_DIRECTORY = "/etc/dataos/secret"
ELASTIC_SEARCH_IO_FORMAT = "org.elasticsearch.spark.sql"
S3_ACCESS_KEY_ID = "spark.hadoop.fs.s3a.access.key"
S3_ACCESS_SECRET_KEY = "spark.hadoop.fs.s3a.secret.key"
S3_SPARK_CONFS = [("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem"),
                  ('spark.hadoop.fs.s3a.aws.credentials.provider',
                   'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider'),
                  ("spark.sql.json.output.committer.class",
                   "org.apache.spark.internal.io.cloud.PathOutputCommitProtocol"),
                  ("spark.hadoop.mapreduce.outputcommitter.factory.scheme.s3a",
                   "org.apache.hadoop.fs.s3a.commit.S3ACommitterFactory"),
                  ("spark.hadoop.fs.s3a.committer.magic.enabled", "true"),
                  ("fs.s3a.committer.name", "magic")
                  ]
S3_ICEBERG_FILE_IO = ("spark.sql.catalog.my_catalog.io-impl", "org.apache.iceberg.aws.s3.S3FileIO")
GCS_ACCOUNT_PRIVATE_KEY_ID = "spark.hadoop.fs.gs.auth.service.account.private.key.id"
GCS_ACCOUNT_PRIVATE_KEY = "spark.hadoop.fs.gs.auth.service.account.private.key"
GCS_ACCOUNT_EMAIL = "spark.hadoop.fs.gs.auth.service.account.email"
GCS_PROJECT_ID = "spark.hadoop.fs.gs.project.id"
GCS_AUTH_ACCOUNT_ENABLED = "spark.hadoop.google.cloud.auth.service.account.enable"
LOG4J_PROPERTIES_DEFAULT_PATH = "/opt/spark/conf/log4j.properties"
LOG4J_PROPERTIES = """log4j.rootLogger={root_logger_level}, console
log4j.logger.org.apache.spark={root_logger_level}
log4j.logger.org.apache.spark.api.python.PythonGatewayServer={root_logger_level}
log4j.appender.console=org.apache.log4j.ConsoleAppender
log4j.appender.console.target=SYSTEM_ERR
log4j.appender.console.layout=org.apache.log4j.PatternLayout
log4j.appender.console.layout.ConversionPattern=[spark][%d{{yyyy - MM - dd HH:mm:ss}}][%p][%c][%m]%n
log4j.appender.publicFile.layout.ConversionPattern=[spark][%p][%d{{yy / MM / dd HH:mm:ss}}][%c][%m]%n
"""


def get_log4j_properties_path():
    return os.environ.get("LOG4J_PROPERTIES_PATH", LOG4J_PROPERTIES_DEFAULT_PATH)


def get_spark_app_name():
    os.environ.get(SPARK_APP_NAME, SPARK_APP_NAME_PREFIX)
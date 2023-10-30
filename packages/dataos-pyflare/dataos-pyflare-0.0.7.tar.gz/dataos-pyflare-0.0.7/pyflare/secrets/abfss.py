
AZURE_STORAGE_ACCOUNT_NAME = "azurestorageaccountname"
AZURE_STORAGE_ACCOUNT_KEY = "azurestorageaccountkey"

SPARK_CONF_AZURE_STORAGE_ACCOUNT_NAME = "fs.azure.account.key.%s.dfs.core.windows.net"


def get_spark_conf(properties: dict):
    conf = dict()
    account_name = get_value_or_throw(AZURE_STORAGE_ACCOUNT_NAME, properties)
    account_key = get_value_or_throw(AZURE_STORAGE_ACCOUNT_KEY, properties)
    spark_conf_storage_name_key = SPARK_CONF_AZURE_STORAGE_ACCOUNT_NAME % account_name
    conf[spark_conf_storage_name_key] = account_key
    return conf


def get_value_or_throw(key: str, data: dict):
    if data[key] is None:
        raise Exception("Key: {0} not found in abfss properties".format(key))
    return data[key]

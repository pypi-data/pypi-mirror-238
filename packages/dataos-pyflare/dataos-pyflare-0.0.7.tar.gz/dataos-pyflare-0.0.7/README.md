# Dataos-PyFlare : DataOS SDK for Apache Spark

### What it does:
Dataos-PyFlare is a powerful Python library designed to simplify data operations and interactions with the DataOS platform and Apache Spark. It provides a convenient and efficient way to load, transform, and save data.

It abstracts out the challenges/complexity around data flow. User can just focus on data transformations and 
business logic.

### Features
* **Streamlined Data Operations**: Dataos-PyFlare streamlines data operations by offering a unified interface for data loading, transformation, and storage, reducing development complexity and time.

* **Data Connector Integration**: Seamlessly connect to various data connectors, including Google BigQuery, Google Cloud Storage (GCS), Snowflake, Redshift, Pulsar and more, using sdk's built-in capabilities.

* **Customizable and Extensible**: Dataos-PyFlare allows for easy customization and extension to suit your specific project requirements. It integrates with existing Python libraries and frameworks for data manipulation.

* **Optimized for DataOS**: Dataos-PyFlare is optimized for the DataOS platform, making it an ideal choice for managing and processing data within DataOS environments.

### Steps to install
Before you begin, make sure you have Python 3 [version >= 3.7] installed on your system.

You can install Dataos-PyFlare and its dependencies using pip:

```
pip install dataos-pyflare
```

Additionally, make sure to have a Spark environment set up with the required configurations for your specific use case.

## Getting Started

### Sample Code:
This code snippet demonstrates how to configure a Dataos-PyFlare session to load data from a source, apply transformations, and save the result to a destination.

```python
from pyflare.sdk import load, save, session_builder

# Define your spark conf params here
sparkConf = [("spark.app.name", "Dataos Sdk Spark App"), ("spark.master", "local[*]"), ("spark.executor.memory", "4g"),
             ("spark.jars.packages", "com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.25.1,"
                                     "com.google.cloud.bigdataoss:gcs-connector:hadoop3-2.2.17,"
                                    "net.snowflake:spark-snowflake_2.12:2.11.0-spark_3.3")
             ]

# Provide dataos token here
token = "bWF5YW5rLjkxYzZiNDQ3LWM3ZWYLWMzNjk3MzQ1MTQyNw=="

# provide dataos fully qualified domain name
DATAOS_FQDN = "sunny-prawn.dataos.app"

# initialize pyflare session
spark = session_builder.SparkSessionBuilder() \
    .with_spark_conf(sparkConf) \
    .with_user_apikey(token) \
    .with_dataos_fqdn(DATAOS_FQDN) \
    .with_depot(depot_name="icebase", acl="r") \
    .with_depot("sanitysnowflake", "rw") \
    .build_session()

# load() method will read dataset city from the source and return a governed dataframe
df_city = load(name="dataos://icebase:retail/city", format="iceberg")

# perform, required transformation as per business logic
df_city = df_city.drop("__metadata")

# save() will write transformed dataset to the sink
save(name="dataos://sanitysnowflake:public/city", mode="overwrite", dataframe=df_city, format="snowflake")
```

### Explanation

1. **Importing Libraries**: We import necessary modules from the pyflare.sdk package.

2. **Spark Configuration**: We define Spark configuration parameters such as the Spark application name, master URL, executor memory, and additional packages required for connectors.

3. **DataOS Token and FQDN**: You provide your DataOS token and fully qualified domain name (FQDN) to authenticate and connect to the DataOS platform.

4. **PyFlare Session Initialization**: We create a PyFlare session using session_builder.SparkSessionBuilder(). This session will be used for data operations.

5. **Loading Data**: We use the load method to load data from a specified source (dataos://icebase:retail/city) in Iceberg format. The result is a governed DataFrame (df_city).

6. **Transformation**: We perform a transformation on the loaded DataFrame by dropping the __metadata column. You can customize this step to fit your business logic.

7. **Saving Data**: Finally, we use the save method to save the transformed DataFrame to a specified destination (dataos://sanitysnowflake:public/customer) in Snowflake format.

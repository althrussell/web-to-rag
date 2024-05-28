# Databricks notebook source
# MAGIC %run ./utils/model_utils

# COMMAND ----------

# MAGIC %run ./00_customer_init

# COMMAND ----------


db_catalog = spark.conf.get("spark.db_catalog")
db_schema = spark.conf.get("spark.db_schema")
db_table = spark.conf.get("spark.db_table")
vs_endpoint = spark.conf.get("spark.vs_endpoint")
embedding_endpoint_name = spark.conf.get("spark.embedding_endpoint_name")
vs_index = spark.conf.get("spark.vs_index")
vs_index_fullname = spark.conf.get("spark.vs_index_fullname")

# COMMAND ----------

print(vs_index_fullname)

# COMMAND ----------

from databricks.vector_search.client import VectorSearchClient

vsc = VectorSearchClient()
# vs_endpoint
vsc.get_endpoint(
  name=vs_endpoint
)

# vs_index = f"{source_table}_bge_index"
# vs_index_fullname = f"{source_catalog}.{source_schema}.{vs_index}"

# COMMAND ----------

index = vsc.create_delta_sync_index(
  endpoint_name=vs_endpoint,
  source_table_name=f'{db_catalog}.{db_schema}.{db_table}',
  index_name=vs_index_fullname,
  pipeline_type='TRIGGERED',
  primary_key="row_id",
  embedding_source_column="content",
  embedding_model_endpoint_name=embedding_endpoint_name
)
index.describe()['status']['message']

# COMMAND ----------

import time
index = vsc.get_index(endpoint_name=vs_endpoint,index_name=vs_index_fullname)
while not index.describe().get('status')['ready']:
  print("Waiting for index to be ready...")
  time.sleep(30)
print("Index is ready!")
index.describe()

# COMMAND ----------



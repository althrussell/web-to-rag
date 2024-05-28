# Databricks notebook source
# MAGIC %pip install --upgrade --force-reinstall databricks-vectorsearch 
# MAGIC

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

#Delta Source Details
source_catalog = "shared"
source_schema = "va_gen_ai_demo"
source_table = "web_scraper_data"

#Vector Search Details
vs_endpoint = "dbdemos_vs_endpoint"
embedding_endpoint_name = "databricks-bge-large-en"

# COMMAND ----------

from databricks.vector_search.client import VectorSearchClient

vsc = VectorSearchClient()
# vs_endpoint
vsc.get_endpoint(
  name=vs_endpoint
)

vs_index = f"{source_table}_bge_index"
vs_index_fullname = f"{source_catalog}.{source_schema}.{vs_index}"

# COMMAND ----------

index = vsc.create_delta_sync_index(
  endpoint_name=vs_endpoint,
  source_table_name=f'{source_catalog}.{source_schema}.{source_table}',
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



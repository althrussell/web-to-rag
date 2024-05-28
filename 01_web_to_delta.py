# Databricks notebook source
# MAGIC %run ./utils/web_scraper

# COMMAND ----------

# MAGIC %run ./00_customer_init

# COMMAND ----------

# Make sure Parameters are correctly defined in 00_customer_init
base_url = spark.conf.get("spark.base_url")
sitemap_url = spark.conf.get("spark.sitemap_url") or None
db_catalog = spark.conf.get("spark.db_catalog")
db_schema = spark.conf.get("spark.db_schema")
db_table = spark.conf.get("spark.db_table")
vs_endpoint = spark.conf.get("spark.vs_endpoint")
embedding_endpoint_name = spark.conf.get("spark.embedding_endpoint_name")


max_depth = 2  # Set the desired maximum depth for scraping if not using sitemap
chunk_size = 1024  # Set the chunk size for text data
overlap = 256  # Set the overlap size for text chunks
scrape_limit = 10  # Set the limit for the number of pages to scrape, or None for no limit
clear_table_flag = True  # Set to True to clear the table before scraping


# COMMAND ----------


# Step 2: Run the scraper

parallel_scrape(base_url, db_catalog, db_schema, db_table, sitemap_url, max_depth, chunk_size, overlap, scrape_limit, clear_table_flag)

# COMMAND ----------



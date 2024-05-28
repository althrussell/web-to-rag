# Databricks notebook source
# MAGIC %run ./utils/web_scraper

# COMMAND ----------

# Make sure Parameters are correctly defined in 00_customer_init
base_url = spark.conf.get("spark.base_url")
sitemap_url = spark.conf.get("spark.sitemap_url") or None
catalog = spark.conf.get("spark.catalog")
schema = spark.conf.get("spark.schema")
table = spark.conf.get("spark.table")
vs_endpoint = spark.conf.get("spark.vs_endpoint")
embedding_endpoint_name = spark.conf.get("spark.embedding_endpoint_name")

# # Step 1: Define parameters
# base_url = ""  # Replace with the URL you want to scrape
# #sitemap_url = "https://www.virginaustralia.com/sitemap-AU.xml"  # Replace with the sitemap URL if available, otherwise use None
# sitemap_url = "https://www.riotinto.com/sitemap.xml"
# catalog = "shared"  # Replace with your catalog name
# schema = "rio_gen_ai_demo"  # Replace with your schema name
# table = "web_scraper_data"  # Replace with your desired table name

max_depth = 2  # Set the desired maximum depth for scraping if not using sitemap
chunk_size = 1024  # Set the chunk size for text data
overlap = 256  # Set the overlap size for text chunks
scrape_limit = None  # Set the limit for the number of pages to scrape, or None for no limit
clear_table_flag = True  # Set to True to clear the table before scraping


# COMMAND ----------


# Step 2: Run the scraper

parallel_scrape(base_url, catalog, schema, table, sitemap_url, max_depth, chunk_size, overlap, scrape_limit, clear_table_flag)

# COMMAND ----------



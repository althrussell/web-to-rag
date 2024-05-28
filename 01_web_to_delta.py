# Databricks notebook source
# MAGIC %run ./utils/web_scraper

# COMMAND ----------


# Step 1: Define parameters
base_url = ""  # Replace with the URL you want to scrape
sitemap_url = "https://www.virginaustralia.com/sitemap-AU.xml"  # Replace with the sitemap URL if available, otherwise use None
catalog = "shared"  # Replace with your catalog name
schema = "va_gen_ai_demo"  # Replace with your schema name
table = "web_scraper_data"  # Replace with your desired table name
max_depth = 2  # Set the desired maximum depth for scraping if not using sitemap
chunk_size = 1024  # Set the chunk size for text data
overlap = 256  # Set the overlap size for text chunks
scrape_limit = 10  # Set the limit for the number of pages to scrape, or None for no limit
clear_table_flag = True  # Set to True to clear the table before scraping


# COMMAND ----------


# Step 2: Run the scraper

parallel_scrape(base_url, catalog, schema, table, sitemap_url, max_depth, chunk_size, overlap, scrape_limit, clear_table_flag)

# COMMAND ----------



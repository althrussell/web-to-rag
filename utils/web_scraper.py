# Databricks notebook source
# MAGIC %pip install beautifulsoup4 requests lxml

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

# web_scraper.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
import re
import uuid
from pyspark.sql import SparkSession
from lxml import etree
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class WebScraper:
    def __init__(self, base_url, sitemap_url=None, chunk_size=1024, overlap=256, max_workers=5):
        self.base_url = base_url
        self.sitemap_url = sitemap_url
        self.visited = set()
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.session = requests.Session()  # Use a session to manage cookies
        self.max_workers = max_workers

    def is_valid(self, url):
        """Check if the URL belongs to the base domain."""
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme) and self.base_url in url

    def get_all_website_links(self, url):
        """Get all valid links from the given URL."""
        urls = set()
        try:
            response = self.session.get(url, headers=self.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                for a_tag in soup.findAll("a"):
                    href = a_tag.attrs.get("href")
                    if href == "" or href is None:
                        continue
                    href = urljoin(url, href)
                    parsed_href = urlparse(href)
                    href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
                    if self.is_valid(href) and href not in self.visited:
                        urls.add(href)
                        self.visited.add(href)
            else:
                print(f"Failed to fetch URL: {url} with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error while requesting URL {url}: {e}")
        return urls

    def get_sitemap_links(self):
        """Get all links from the sitemap URL."""
        urls = set()
        retries = 3
        for attempt in range(retries):
            try:
                response = self.session.get(self.sitemap_url, headers=self.headers)
                if response.status_code == 200:
                    content = response.content
                    print(f"Sitemap content: {content[:500]}...")  # Log first 500 characters of the content
                    root = etree.fromstring(content)
                    for url in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
                        loc = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
                        if self.is_valid(loc):
                            urls.add(loc)
                    break
                else:
                    print(f"Failed to fetch sitemap: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Error while requesting sitemap URL {self.sitemap_url}: {e}")
            except etree.XMLSyntaxError as e:
                print(f"Error parsing sitemap XML from {self.sitemap_url}: {e}")
            if attempt < retries - 1:
                print("Retrying...")
                time.sleep(5)
        return urls

    def chunk_text(self, text):
        """Chunk the text into manageable pieces with overlap."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            if end >= len(text):
                chunks.append(text[start:])
                break
            else:
                end = text.rfind(' ', start, end)
                if end == -1:
                    end = start + self.chunk_size
                chunk = text[start:end].strip()
                chunks.append(chunk)
                start = end - self.overlap
        return chunks

    def scrape_page(self, url):
        """Scrape the page content and chunk the text."""
        try:
            response = self.session.get(url, headers=self.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                page_text = soup.get_text(separator="\n", strip=True)
                page_text = re.sub(r'\s+', ' ', page_text)  # Remove extra whitespace
                scrape_time = datetime.now()
                text_chunks = self.chunk_text(page_text)
                return [{"row_id": str(uuid.uuid4()), "url": url, "content": chunk, "scrape_time": scrape_time} for chunk in text_chunks]
            else:
                print(f"Failed to fetch URL: {url} with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error while scraping URL {url}: {e}")
        return []

def catalog_exists(catalog_name):
    """Check if the catalog exists."""
    try:
        catalogs = spark.sql(f"SHOW CATALOGS LIKE '{catalog_name}'")
        return catalogs.filter(catalogs.catalog.contains(catalog_name)).count() > 0
    except Exception as e:
        print(f"Error while checking catalog {catalog_name}: {e}")
        return False

def schema_exists(catalog_name, schema_name):
    """Check if the schema exists within the catalog."""
    try:
        schemas = spark.sql(f"SHOW SCHEMAS IN {catalog_name} LIKE '{schema_name}'")
        return schemas.filter(schemas.databaseName.contains(schema_name)).count() > 0
    except Exception as e:
        print(f"Error while checking schema {schema_name} in catalog {catalog_name}: {e}")
        return False

def table_exists(catalog, schema, table):
    """Check if the table exists."""
    try:
        tables = spark.sql(f"SHOW TABLES IN {catalog}.{schema} LIKE '{table}'")
        return tables.filter(tables.tableName.contains(table)).count() > 0
    except Exception as e:
        print(f"Error while checking table {table} in schema {schema}: {e}")
        return False

def create_catalog_and_schema_if_not_exists(catalog, schema):
    """Create catalog and schema if they do not exist."""
    if not catalog_exists(catalog):
        spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog}")
    if not schema_exists(catalog, schema):
        spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")

def create_table_if_not_exists(catalog, schema, table):
    """Create table if it does not exist and enable Change Data Feed."""
    full_table_name = f"{catalog}.{schema}.{table}"
    if not table_exists(catalog, schema, table):
        try:
            spark.sql(f"""
                CREATE TABLE {full_table_name} (
                    row_id STRING,
                    url STRING,
                    content STRING,
                    scrape_time TIMESTAMP
                )
                USING DELTA
                TBLPROPERTIES (delta.enableChangeDataFeed = true)
            """)
            print(f"Table {full_table_name} created with Change Data Feed enabled")
        except Exception as e:
            print(f"Error while creating table {full_table_name}: {e}")

def clear_table(catalog, schema, table):
    """Clear the target table if it exists."""
    full_table_name = f"{catalog}.{schema}.{table}"
    try:
        spark.sql(f"DROP TABLE IF EXISTS {full_table_name}")
        print(f"Cleared table {full_table_name}")
    except Exception as e:
        print(f"Error while clearing table {full_table_name}: {e}")

def enable_cdf(catalog, schema, table):
    """Enable Change Data Feed on the Delta table."""
    full_table_name = f"{catalog}.{schema}.{table}"
    try:
        spark.sql(f"ALTER TABLE {full_table_name} SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")
        print(f"Enabled Change Data Feed on table {full_table_name}")
    except Exception as e:
        print(f"Error while enabling Change Data Feed on table {full_table_name}: {e}")

def write_to_delta(text_data_list, catalog, schema, table):
    """Write the scraped data to a Delta table."""
    full_table_name = f"{catalog}.{schema}.{table}"
    try:
        table_schema = StructType([
            StructField("row_id", StringType(), True),
            StructField("url", StringType(), True),
            StructField("content", StringType(), True),
            StructField("scrape_time", TimestampType(), True)
        ])
        df = spark.createDataFrame(text_data_list, schema=table_schema)
        df.write.format("delta").mode("append").saveAsTable(full_table_name)
        print(f"Data successfully written to Delta table {full_table_name}")
    except Exception as e:
        print(f"Error while writing to Delta table {full_table_name}: {e}")

def parallel_scrape(base_url, catalog, schema, table, sitemap_url=None, max_depth=2, chunk_size=1024, overlap=256, scrape_limit=None, clear_table_flag=False, max_workers=5):
    """Perform parallel scraping using Spark."""
    scraper = WebScraper(base_url, sitemap_url, chunk_size, overlap, max_workers)

    create_catalog_and_schema_if_not_exists(catalog, schema)

    if clear_table_flag:
        clear_table(catalog, schema, table)
        create_table_if_not_exists(catalog, schema, table)
    else:
        if table_exists(catalog, schema, table):
            enable_cdf(catalog, schema, table)
        else:
            create_table_if_not_exists(catalog, schema, table)

    if sitemap_url:
        initial_links = scraper.get_sitemap_links()
    else:
        initial_links = scraper.get_all_website_links(base_url)

    all_links = set(initial_links)
    current_links = initial_links
    if not sitemap_url:  # Only expand links if not using sitemap
        for _ in range(max_depth):
            new_links = set()
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(scraper.get_all_website_links, url): url for url in current_links}
                for future in as_completed(futures):
                    new_links.update(future.result())
            new_links -= all_links
            all_links.update(new_links)
            current_links = new_links

    # Apply scrape limit if provided
    if scrape_limit is not None:
        all_links = list(all_links)[:scrape_limit]

    # Collect data and write to Delta for each page
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scraper.scrape_page, url): url for url in all_links}
        for future in as_completed(futures):
            page_data = future.result()
            if page_data:
                write_to_delta(page_data, catalog, schema, table)


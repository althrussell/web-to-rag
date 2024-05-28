# Databricks notebook source
# Initialize for Specific Customer Demo

# Step 1: Define parameters
base_url = ""  # Replace with the URL you want to scrape
sitemap_url = "" # Replace with the sitemap URL if available, otherwise use None

#Unity Catalog Details
catalog = "shared"  # Replace with your catalog name
schema = "va_gen_ai_demo"  # Replace with your schema name
table = "web_scraper_data"  # Replace with your desired table name

#Vector Search Details
vs_endpoint = "dbdemos_vs_endpoint"
embedding_endpoint_name = "databricks-bge-large-en"

vs_index = f"{table}_bge_index"
vs_index_fullname = f"{catalog}.{schema}.{vs_index}"

# COMMAND ----------

# Define Questions and Roles
user_questions = [
    "Can I bring my 80kg dog onboard?",
    "What are the baggage restrictions for international flights?"
]

contexts = [
    "",
    "International flights often have stricter baggage policies."
]

system_roles = [
    "You are an experienced travel agent that takes a conversation between a traveller and yourself and answer their questions based on the below context.",
    "You are a knowledgeable customer service representative with expertise in airline policies."
]

system_instructions = [
    """- Do not answer saying 'Based on the context provided'
         - If there is a context provided. Focus your answers based on the context but provide additional helpful notes from your background knowledge caveat those notes though.
         - If there is no context use question and source data to answer.
         - If the context does not seem relevant to the answer say as such.""",
          "Provide a concise answer."

]
# Create an instance of RagContext

# COMMAND ----------

# Set as Spark Variables
spark.conf.set("spark.base_url", base_url)
spark.conf.set("spark.sitemap_url", sitemap_url)

spark.conf.set("spark.catalog", catalog)
spark.conf.set("spark.schema", schema)
spark.conf.set("spark.table", table)

spark.conf.set("spark.vs_endpoint", vs_endpoint)
spark.conf.set("spark.embedding_endpoint_name", embedding_endpoint_name)

spark.conf.set("spark.vs_index", vs_index)
spark.conf.set("spark.vs_index_fullname", vs_index_fullname)

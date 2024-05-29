# Databricks notebook source
# Initialize for Specific Customer Demo

# Step 1: Define parameters
base_url = ""  # Replace with the URL you want to scrape
sitemap_url = "" # Replace with the sitemap URL if available, otherwise use None

#Unity Catalog Details
db_catalog = "shared"  # Replace with your catalog name
db_schema = "rio_gen_ai_demo"  # Replace with your schema name
db_table = "web_scraper_data"  # Replace with your desired table name

#Vector Search Details
vs_endpoint = "dbdemos_vs_endpoint"
embedding_endpoint_name = "databricks-bge-large-en"

vs_index = f"{db_table}_bge_index"
vs_index_fullname = f"{db_catalog}.{db_schema}.{vs_index}"



# COMMAND ----------



# COMMAND ----------

# Define Questions and Roles
user_questions = [
    "What are the latest safety statistics for Rio Tinto?",
    "How does Rio Tinto measure and report safety performance?",
    "What is Rio Tinto's Total Recordable Injury Frequency Rate (TRIFR)?",
    "How has Rio Tinto's safety performance changed over the past five years?",
    "What are the main causes of workplace injuries at Rio Tinto?",
    "How does Rio Tinto ensure the safety of its employees and contractors?",
    "What safety training programs does Rio Tinto implement?",
    "How does Rio Tinto track and respond to safety incidents?",
    "What safety awards or recognitions has Rio Tinto received?",
    "How does Rio Tinto involve employees in safety initiatives?",
    "What are the key components of Rio Tinto's ESG strategy?",
    "How does Rio Tinto address environmental sustainability in its operations?",
    "What is Rio Tinto's policy on reducing greenhouse gas emissions?",
    "How does Rio Tinto manage water usage and conservation?",
    "What measures does Rio Tinto take to protect biodiversity?",
    "How does Rio Tinto ensure responsible sourcing of materials?",
    "What are Rio Tinto's policies regarding human rights and labor practices?",
    "How does Rio Tinto engage with local communities?",
    "What governance structures are in place to oversee ESG efforts at Rio Tinto?",
    "How does Rio Tinto report its ESG performance to stakeholders?",
    "What sustainability goals has Rio Tinto set for the next decade?",
    "How does Rio Tinto integrate sustainability into its business strategy?",
    "What renewable energy projects is Rio Tinto involved in?",
    "How does Rio Tinto handle waste management and recycling?",
    "What are some examples of Rio Tinto's sustainable mining practices?",
    "How does Rio Tinto support sustainable development in the regions where it operates?",
    "What partnerships does Rio Tinto have with environmental organizations?",
    "How does Rio Tinto promote sustainability innovation and technology?",
    "What progress has Rio Tinto made in achieving its sustainability targets?",
    "How does Rio Tinto's sustainability performance compare to industry benchmarks?"
]



contexts = [
    "",
    "International flights often have stricter baggage policies."
]

system_roles = [
    "You are an experienced travel agent that takes a conversation between a traveller and yourself and answer their questions based on the below context.",
    "You are a knowledgeable customer service representative with expertise in airline policies.",
    "You are a knowledgeable and helpful assistant specializing in providing detailed information about companies' safety statistics, ESG policies, and sustainability actions. Answer the following questions about Rio Tinto with precise and accurate information, ensuring clarity and comprehensiveness in your responses."
]

system_instructions = [
    """- Do not answer saying 'Based on the context provided'
         - If there is a context provided. Focus your answers based on the context but provide additional helpful notes from your background knowledge caveat those notes though.
         - If there is no context use question and source data to answer.
         - If the context does not seem relevant to the answer say as such.""",
          "Provide a polite and respectful response.",
          ""

]


# COMMAND ----------

# Set as Spark Variables
spark.conf.set("spark.base_url", base_url)
spark.conf.set("spark.sitemap_url", sitemap_url)

spark.conf.set("spark.db_catalog", db_catalog)
spark.conf.set("spark.db_schema", db_schema)
spark.conf.set("spark.db_table", db_table)

spark.conf.set("spark.vs_endpoint", vs_endpoint)
spark.conf.set("spark.embedding_endpoint_name", embedding_endpoint_name)

spark.conf.set("spark.vs_index", vs_index)
spark.conf.set("spark.vs_index_fullname", vs_index_fullname)

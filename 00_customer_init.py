# Databricks notebook source
# Initialize for Specific Customer Demo

# Step 1: Define parameters
base_url = ""  # Replace with the URL you want to scrape
sitemap_url = "https://www.virginaustralia.com/sitemap-AU.xml" # Replace with the sitemap URL if available, otherwise use None

#Unity Catalog Details
db_catalog = "shared"  # Replace with your catalog name
db_schema = "va_gen_ai_demo"  # Replace with your schema name
db_table = "web_scraper_data"  # Replace with your desired table name

#Vector Search Details
vs_endpoint = "dbdemos_vs_endpoint"
embedding_endpoint_name = "databricks-bge-large-en"

vs_index = f"{db_table}_bge_index"
vs_index_fullname = f"{db_catalog}.{db_schema}.{vs_index}"



# COMMAND ----------

# Define Questions and Roles
user_questions = [
    "What is the headquarters location of Virgin Australia?",
    "How many destinations does Virgin Australia serve?",
    "What is the fleet size of Virgin Australia?",
    "Does Virgin Australia offer a loyalty program?",
    "What is the name of Virgin Australia's loyalty program?",
    "What are the benefits of joining Virgin Australia's Velocity Frequent Flyer program?",
    "Can you earn points with Virgin Australia's Velocity Frequent Flyer program on partner airlines?",
    "What are the classes of service offered by Virgin Australia?",
    "Does Virgin Australia offer in-flight entertainment?",
    "What are the amenities provided in Virgin Australia's business class?",
    "Does Virgin Australia provide Wi-Fi on their flights?",
    "Can you book special meals on Virgin Australia flights?",
    "How can you check in for a Virgin Australia flight?",
    "What is the baggage allowance for Virgin Australia flights?",
    "Does Virgin Australia have a mobile app?",
    "What are the features of the Virgin Australia mobile app?",
    "Does Virgin Australia offer airport lounge access?",
    "What are the names of Virgin Australia's airport lounges?",
    "Can you purchase extra legroom seats on Virgin Australia flights?",
    "Does Virgin Australia have a codeshare agreement with other airlines?",
    "Which airlines does Virgin Australia have codeshare agreements with?",
    "What are Virgin Australia's policies for traveling with pets?",
    "Does Virgin Australia offer group booking options?",
    "Can you change or cancel a booking with Virgin Australia?",
    "What are the fees for changing or canceling a booking with Virgin Australia?",
    "Does Virgin Australia have a frequent flyer program for corporate travelers?",
    "What is the name of Virgin Australia's corporate frequent flyer program?",
    "Can you use Velocity Frequent Flyer points to upgrade your seat on Virgin Australia flights?",
    "Does Virgin Australia have a partnership with any car rental companies?",
    "How can you earn Velocity Frequent Flyer points with Virgin Australia's partners?",
    "What are Virgin Australia's policies for unaccompanied minors?",
    "Does Virgin Australia offer any special assistance for passengers with disabilities?",
    "What is Virgin Australia's policy on electronic devices during flights?",
    "Can you book Virgin Australia flights through travel agents?",
    "Does Virgin Australia have a credit card program?",
    "What are the benefits of the Virgin Australia credit card?",
    "Does Virgin Australia offer holiday packages?",
    "What is included in Virgin Australia's holiday packages?",
    "How can you contact Virgin Australia's customer service?",
    "Does Virgin Australia have a lost and found service?",
    "What are Virgin Australia's policies for delayed or canceled flights?",
    "Can you get a refund for a canceled Virgin Australia flight?",
    "Does Virgin Australia offer travel insurance?",
    "What are the benefits of purchasing travel insurance through Virgin Australia?",
    "How can you join Virgin Australia's Velocity Frequent Flyer program?",
    "Does Virgin Australia offer any in-flight magazines or reading materials?",
    "Can you bring duty-free items on Virgin Australia flights?",
    "What are the requirements for traveling with infants on Virgin Australia flights?",
    "Does Virgin Australia offer any promotions or discounts?",
    "How can you stay updated on Virgin Australia's latest news and offers?"
]


contexts = [
    "",
    "International flights often have stricter baggage policies."
]

system_roles = [
    "You are an experienced travel agent that takes a conversation between a traveller and yourself and answer their questions based on the below context.",
    "You are a knowledgeable customer service representative with expertise in airline policies.",
    "You are a Rio Tinto expert. You know mining and the resources industry."
]

system_instructions = [
    """- Do not answer saying 'Based on the context provided'
         - If there is a context provided. Focus your answers based on the context but provide additional helpful notes from your background knowledge caveat those notes though.
         - If there is no context use question and source data to answer.
         - If the context does not seem relevant to the answer say as such.""",
          "Provide a polite and respectful response."

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

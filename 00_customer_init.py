# Databricks notebook source
# Initialize for Specific Customer Demo

# Step 1: Define parameters
base_url = ""  # Replace with the URL you want to scrape
# sitemap_url = "https://www.bcf.com.au/sitemap_0-product.xml" # Replace with the sitemap URL if available, otherwise use None

#Unity Catalog Details
db_catalog = "shared"  # Replace with your catalog name
db_schema = "bcf_gen_ai_demo"  # Replace with your schema name
db_table = "web_scraper_data"  # Replace with your desired table name

#Vector Search Details
vs_endpoint = "dbdemos_vs_endpoint"
embedding_endpoint_name = "databricks-bge-large-en"

vs_index = f"{db_table}_bge_index"
vs_index_fullname = f"{db_catalog}.{db_schema}.{vs_index}"



# COMMAND ----------

#DONE - sitemap_url = "https://www.bcf.com.au/sitemap_0-product.xml"
sitemap_url = "https://www.bcf.com.au/sitemap_1-product.xml"
#DONE - sitemap_url = "https://www.bcf.com.au/sitemap_2-product.xml"
#NOT REQ -  sitemap_url = "https://www.bcf.com.au/sitemap_3-image.xml"
#NOT REQ -  sitemap_url = "https://www.bcf.com.au/sitemap_4-image.xml"
#NOT REQ -  sitemap_url = "https://www.bcf.com.au/sitemap_5-image.xml"
#INCOMPLETE - sitemap_url = "https://www.bcf.com.au/sitemap_6-category.xml"
#DONE - sitemap_url = "https://www.bcf.com.au/sitemap_7-content.xml"
#DONE - sitemap_url = "https://www.bcf.com.au/sitemap_8-folder.xml"
#DONE - sitemap_url = "https://www.bcf.com.au/sitemap_9.xml"
#DONE - sitemap_url = "https://www.bcf.com.au/sitemap-stores.xml"

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
    "What is Rio Tinto's policy on near-miss reporting?",
    "How does Rio Tinto use technology to improve safety?",
    "What are the key elements of Rio Tinto's safety culture?",
    "How does Rio Tinto benchmark its safety performance against industry standards?",
    "What are the most common types of accidents at Rio Tinto operations?",
    "How does Rio Tinto manage safety risks in remote locations?",
    "What personal protective equipment (PPE) standards does Rio Tinto enforce?",
    "How does Rio Tinto ensure safety compliance among contractors?",
    "What are Rio Tinto's emergency response procedures?",
    "How does Rio Tinto promote mental health and well-being among its employees?",
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
    "How does Rio Tinto's sustainability performance compare to industry benchmarks?",
    "What are Rio Tinto's policies on climate change?",
    "How does Rio Tinto assess the environmental impact of its operations?",
    "What are Rio Tinto's key initiatives in renewable energy?",
    "How does Rio Tinto contribute to the circular economy?",
    "What are the main environmental challenges faced by Rio Tinto?",
    "How does Rio Tinto manage its carbon footprint?",
    "What is Rio Tinto's approach to corporate social responsibility?",
    "How does Rio Tinto support local economies?",
    "What diversity and inclusion initiatives does Rio Tinto have in place?",
    "How does Rio Tinto ensure ethical business practices?",
    "What are Rio Tinto's financial performance metrics for the last fiscal year?",
    "What is Rio Tinto's revenue and profit trend over the past five years?",
    "How does Rio Tinto manage its financial risks?",
    "What are the key markets for Rio Tinto's products?",
    "How does Rio Tinto's stock performance compare to its industry peers?",
    "What is Rio Tinto's dividend policy?",
    "How does Rio Tinto allocate its capital expenditures?",
    "What are the main products and services offered by Rio Tinto?",
    "What are the major projects Rio Tinto is currently working on?",
    "How does Rio Tinto ensure operational efficiency?",
    "What technological advancements is Rio Tinto investing in?",
    "How does Rio Tinto manage its supply chain?",
    "What are Rio Tinto's policies on cybersecurity and data protection?",
    "How does Rio Tinto address geopolitical risks?",
    "What are Rio Tinto's corporate governance practices?",
    "Who are the key executives at Rio Tinto?",
    "How does Rio Tinto ensure transparency in its operations?",
    "What is Rio Tinto's approach to stakeholder engagement?",
    "What are the major challenges faced by Rio Tinto?",
    "How does Rio Tinto plan to grow its business in the future?",
    "What innovations is Rio Tinto known for?",
    "How does Rio Tinto approach research and development?",
    "What is Rio Tinto's policy on mergers and acquisitions?",
    "How does Rio Tinto contribute to industry standards and regulations?",
    "What is Rio Tinto's approach to crisis management?",
    "How does Rio Tinto manage its human resources?",
    "What are the key performance indicators used by Rio Tinto?",
    "How does Rio Tinto ensure customer satisfaction?",
    "What are Rio Tinto's marketing and sales strategies?",
    "What is Rio Tinto's approach to brand management?",
    "How does Rio Tinto engage with investors?",
    "What are the future trends that could impact Rio Tinto's business?",
    "How does Rio Tinto leverage big data and analytics?",
    "What sustainability certifications has Rio Tinto achieved?",
    "How does Rio Tinto participate in global sustainability initiatives?",
    "What are Rio Tinto's policies on anti-corruption?",
    "How does Rio Tinto handle conflicts of interest?",
    "What are the training and development programs offered by Rio Tinto?",
    "How does Rio Tinto support innovation and creativity within the company?",
    "What are Rio Tinto's strategies for reducing operational costs?",
    "How does Rio Tinto evaluate the effectiveness of its ESG initiatives?",
    "What are the recent awards and recognitions received by Rio Tinto?",
    "How does Rio Tinto balance short-term performance with long-term sustainability?",
    "What are Rio Tinto's strategies for entering new markets?",
    "How does Rio Tinto manage its intellectual property?",
    "What are the community development projects supported by Rio Tinto?",
    "How does Rio Tinto address labor relations and union engagements?",
    "What are the environmental compliance standards followed by Rio Tinto?"
]




contexts = [
    "",
    "International flights often have stricter baggage policies."
]

system_roles = [
    "You are an experienced travel agent that takes a conversation between a traveller and yourself and answer their questions based on the below context.",
    "You are a knowledgeable customer service representative with expertise in airline policies.",
    "You are a knowledgeable and helpful assistant specializing in providing detailed information about companies' safety statistics, ESG policies, and sustainability actions. Answer the following questions about Rio Tinto with precise and accurate information, ensuring clarity and comprehensiveness in your responses.",
    "You are a knowledgeable and helpful assistant"
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

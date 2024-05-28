# Databricks notebook source
# MAGIC %pip install -U mlflow==2.13.0 langchain langchain-community databricks-vectorsearch #llama_index

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

from langchain_community.chat_models import ChatDatabricks
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.embeddings import DatabricksEmbeddings

from databricks.vector_search.client import VectorSearchClient
from langchain_community.vectorstores import DatabricksVectorSearch

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# COMMAND ----------

class Model:
    def __init__(self, name, endpoint, target_uri, temperature):
        self.name = name
        self.endpoint = endpoint
        self.target_uri = target_uri
        self.temperature = temperature


# COMMAND ----------

llama = Model("llama", "databricks-meta-llama-3-70b-instruct","databricks",0.1)
mixtral = Model("mixtral", "databricks-mixtral-8x7b-instruct","databricks",0.1)
dbrx = Model("dbrx", "databricks-dbrx-instruct","databricks",0.1)



# COMMAND ----------

import json

class Questions:
    _questions = None

    @classmethod
    def _load_questions(cls):
        if cls._questions is None:
            with open('./utils/questions.json', 'r') as file:
                cls._questions = json.load(file)

    @classmethod
    def get_questions(cls, category):
        cls._load_questions()
        return cls._questions.get(category, ["Category not found"])

# COMMAND ----------

def display_chat(chat_history, response):
    def user_message_html(message):
        return f"""
            <div style="width: 90%; border-radius: 10px; background-color: #c2efff; padding: 10px; box-shadow: 2px 2px 2px #F7f7f7; margin-bottom: 10px; font-size: 14px;">
                {message}
            </div>"""
    
    def assistant_message_html(message):
        return f"""
            <div style="width: 90%; border-radius: 10px; background-color: #e3f6fc; padding: 10px; box-shadow: 2px 2px 2px #F7f7f7; margin-bottom: 10px; margin-left: 40px; font-size: 14px">
                <img style="float: left; width:40px; margin: -10px 5px 0px -10px" src="https://github.com/databricks-demos/dbdemos-resources/blob/main/images/product/chatbot-rag/robot.png?raw=true"/>
                {message}
            </div>"""
    
    chat_history_html = "".join([user_message_html(m["content"]) if m["role"] == "user" else assistant_message_html(m["content"]) for m in chat_history])
    input_message = response["input"].replace('\n', '<br/>')
    answer = response["answer"].replace('\n', '<br/>')

    unique_urls = set(doc.metadata['url'] for doc in response['context'])
    sources_html = ("<br/><br/><br/><strong>Sources:</strong><br/> <ul>" + '\n'.join([f"""<li><a href="{url}">{url}</a></li>""" for url in unique_urls]) + "</ul>")

    response_html = f"""{answer}{sources_html}"""

    displayHTML(chat_history_html + user_message_html(input_message) + assistant_message_html(response_html))



# Databricks notebook source
# MAGIC %pip install -U mlflow==2.13.0 langchain langchain-community databricks-vectorsearch openai-whisper gradio typing-extensions uvicorn fastapi mlflow[databricks]
# MAGIC

# COMMAND ----------

#pip install git+https://github.com/openai/whisper.git

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

bannerColor = '#103a63ff'
chatboxColor = '#efefefff'
customer_name = 'BCF'
#https://github.com/databricks-demos/dbdemos-resources/blob/main/images/product/chatbot-rag/robot.png?raw=true
imgurl = 'https://www.bcf.com.au/on/demandware.static/-/Library-Sites-bcf-shared-library/default/dw68c7ebb7/images/global-navigation/header/BCF_Logo.svg'

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

#custom
mix8_pt = Model("mix_pt","va_genai_demo","databricks",0.1)
mix7_pt = Model("mix7_pt","va_mixtral_demo","databricks",0.1)


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
            <div style="width: 90%; border-radius: 10px; background-color: {bannerColor}; padding: 10px; box-shadow: 2px 2px 2px #F7f7f7; margin-bottom: 10px; font-size: 14px; color: white;">
                {message}
            </div>"""
    
    def assistant_message_html(message):
        return f"""
            <div style="width: 90%; border-radius: 10px; background-color: {chatboxColor}; padding: 10px; box-shadow: 2px 2px 2px #F7f7f7; margin-bottom: 10px; margin-left: 40px; font-size: 14px">
                <img style="float: left; width:80px; margin: 5px 5px 5px 5px" src="{imgurl}"/>
                {message}
            </div>"""
    
    chat_history_html = "".join([user_message_html(m["content"]) if m["role"] == "user" else assistant_message_html(m["content"]) for m in chat_history])
    input_message = response["input"].replace('\n', '<br/>')
    answer = response["answer"].replace('\n', '<br/>')

    unique_urls = set(doc.metadata['url'] for doc in response['context'])
    sources_html = ("<br/><br/><br/><strong>Sources:</strong><br/> <ul>" + '\n'.join([f"""<li><a href="{url}">{url}</a></li>""" for url in unique_urls]) + "</ul>")

    response_html = f"""{answer}{sources_html}"""

    displayHTML(chat_history_html + user_message_html(input_message) + assistant_message_html(response_html))



# COMMAND ----------

def display_basic_chat(input, response):
    def user_message_html(message):
        return f"""
            <div style="width: 90%; border-radius: 10px; background-color: {bannerColor}; padding: 10px; box-shadow: 2px 2px 2px #F7f7f7; margin-bottom: 10px; font-size: 14px; color: white;">
                {message}
            </div>"""
    
    def assistant_message_html(message):
        return f"""
            <div style="width: 90%; border-radius: 10px; background-color: {chatboxColor}; padding: 10px; box-shadow: 2px 2px 2px #F7f7f7; margin-bottom: 10px; margin-left: 40px; font-size: 14px">
                <img style="float: left; width:80px; margin: 5px 5px 5px 5px" src="{imgurl}"/>
                {message}
            </div>"""
    
    
    input_message = input.replace('\n', '<br/>')
    answer = response.replace('\n', '<br/>')

    response_html = f"""{answer}"""

    displayHTML(user_message_html(input_message) + assistant_message_html(response_html))



# COMMAND ----------

class RagContext:
    def __init__(self, user_questions, contexts, system_roles, system_instructions):
        self.user_questions = user_questions
        self.contexts = contexts
        self.system_roles = system_roles
        self.system_instructions = system_instructions

    def get_context(self, user_question_index, context_index, system_role_index, system_instruction_index):
        return {
            "user_question": self.user_questions[user_question_index],
            "context": self.contexts[context_index],
            "system_role": self.system_roles[system_role_index],
            "system_instruction": self.system_instructions[system_instruction_index]
        }


# COMMAND ----------

def call_llm_with_context(retrieval_chain,rag_context, user_question_index, context_index, system_role_index, system_instruction_index):
    context_data = rag_context.get_context(user_question_index, context_index, system_role_index, system_instruction_index)
    response = retrieval_chain.invoke({
        "chat_history": [],
        "input": context_data["user_question"],
        "context": context_data["context"],
        "system_role": context_data["system_role"],
        "system_instruction": context_data["system_instruction"]
    })
    return response

# COMMAND ----------

def call_llm_with_text(retrieval_chain,rag_context, user_question, context_index, system_role_index, system_instruction_index):
    context_data = rag_context.get_context(0, context_index, system_role_index, system_instruction_index)
    response = retrieval_chain.invoke({
        "chat_history": [],
        "input": user_question,
        "context": context_data["context"],
        "system_role": context_data["system_role"],
        "system_instruction": context_data["system_instruction"]
    })
    return response

# COMMAND ----------



# Databricks notebook source
# MAGIC %run ./utils/model_utils

# COMMAND ----------

## SET WHICH MODEL TO USE
# llama, mixtral, dbrx
model = mixtral

# COMMAND ----------

# MAGIC %run ./utils/00_setup

# COMMAND ----------

# db_catalog = spark.conf.get("spark.db_catalog")
# db_schema = spark.conf.get("spark.db_schema")
# db_table = spark.conf.get("spark.db_table")
# vs_endpoint = spark.conf.get("spark.vs_endpoint")
# embedding_endpoint_name = spark.conf.get("spark.embedding_endpoint_name")
# vs_index = spark.conf.get("spark.vs_index")
# vs_index_fullname = spark.conf.get("spark.vs_index_fullname")
# rag_context = RagContext(user_questions, contexts, system_roles, system_instructions)

# COMMAND ----------

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatDatabricks

TEMPLATE = """You are an assistant for BCF (Boating Camping Fishing) customers. You are answering boating, camping, general outdoors and fishing question.. If the question is not related to one of these topics, kindly decline to answer. If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use the following pieces of context to answer the question at the end, use the context to recommend BCF products:
{context}
Question: {question}
Answer:
"""
prompt = PromptTemplate(template=TEMPLATE, input_variables=["context", "question"])

chain = RetrievalQA.from_chain_type(
    llm=chat,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt}
)

# COMMAND ----------

question = {"query": "How do I catch a fish in moreton bay?"}
answer = chain.invoke(question)
print(answer)

# COMMAND ----------

from mlflow.models import infer_signature
import mlflow
import langchain

mlflow.set_registry_uri("databricks-uc")
model_name = f"{db_catalog}.{db_schema}.rag_chatbot_mixtral_model"

with mlflow.start_run(run_name="rag_chatbot_model") as run:
    signature = infer_signature(question, answer)
    model_info = mlflow.langchain.log_model(
        chain,
        loader_fn=get_retriever,  # Load the retriever with DATABRICKS_TOKEN env as secret (for authentication).
        artifact_path="chain",
        registered_model_name=model_name,
        pip_requirements=[
            "mlflow==" + mlflow.__version__,
            "langchain==" + langchain.__version__,
            "databricks-vectorsearch",
        ],
        input_example=question,
        signature=signature
    )

# COMMAND ----------

os.environ['API_ENDPOINT'] = "https://e2-demo-west.cloud.databricks.com/serving-endpoints/bcf-demo-llama-chat/invocations"

# COMMAND ----------

!python3 ./utils/app.py

# COMMAND ----------



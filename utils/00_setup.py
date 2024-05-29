# Databricks notebook source
# MAGIC %run ./../00_customer_init

# COMMAND ----------

db_catalog = spark.conf.get("spark.db_catalog")
db_schema = spark.conf.get("spark.db_schema")
db_table = spark.conf.get("spark.db_table")
vs_endpoint = spark.conf.get("spark.vs_endpoint")
embedding_endpoint_name = spark.conf.get("spark.embedding_endpoint_name")
vs_index = spark.conf.get("spark.vs_index")
vs_index_fullname = spark.conf.get("spark.vs_index_fullname")
rag_context = RagContext(user_questions, contexts, system_roles, system_instructions)

# COMMAND ----------

chat = ChatDatabricks(
    target_uri=model.target_uri,
    endpoint=model.endpoint,
    temperature=model.temperature,
)

# COMMAND ----------

vsc = VectorSearchClient(disable_notice=True)
index = vsc.get_index(endpoint_name=vs_endpoint,
                      index_name=vs_index_fullname)

retriever = DatabricksVectorSearch(
    index, text_column="content", 
     columns=["url"]
).as_retriever()

retriever_prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a response to answer this question")
    ])

retriever_chain = create_history_aware_retriever(chat, retriever, retriever_prompt)

# COMMAND ----------

from operator import itemgetter
from langchain.schema.runnable import RunnableBranch, RunnableLambda, RunnableParallel, RunnablePassthrough
def extract_question(input):
    return input[-1]["content"]
  
retrieve_document_chain = (
    itemgetter("messages")
    | RunnableLambda(extract_question)
    | retriever
)



# COMMAND ----------



prompt_template = ChatPromptTemplate.from_messages([
        ("system", """
         {system_role}:
         
         <context>
         {context}
         </context> 
         
         <instructions>
         {system_instruction}
         </instructions>
         """),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])

stuff_documents_chain = create_stuff_documents_chain(chat, prompt_template)

retrieval_chain = create_retrieval_chain(retriever_chain, stuff_documents_chain)

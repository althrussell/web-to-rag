# Databricks notebook source
# MAGIC %run ./utils/model_utils

# COMMAND ----------

#Delta Source Details
db_catalog = 'shared'
db_schema = 'va_gen_ai_demo'
db_table = "web_scraper_data"

#Vector Search Details
endpoint_name = "dbdemos_vs_endpoint"
vs_index = f"{db_table}_bge_index"
#embedding_model = "databricks-bge-large-en"
vs_index_fullname = f"{db_catalog}.{db_schema}.{vs_index}"

# COMMAND ----------

## SET WHICH MODEL TO USE
# llama, mixtral, dbrx
model = llama

chat = ChatDatabricks(
    target_uri=model.target_uri,
    endpoint=model.endpoint,
    temperature=model.temperature,
)
#embeddings = DatabricksEmbeddings(endpoint=embedding_model)

# COMMAND ----------

# MAGIC %md ## Setting Up chain

# COMMAND ----------

vsc = VectorSearchClient(disable_notice=True)
index = vsc.get_index(endpoint_name=endpoint_name,
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

system_role = "You are a experienced travel agent that takes a conversation between a traveller and yourself and answer their questions based on the below context"

# COMMAND ----------



prompt_template = ChatPromptTemplate.from_messages([
        ("system", """
         {system_role}:
         
         <context>
         {context}
         </context> 
         
         <instructions>
         - Focus your answers based on the context but provide additional helpful notes from your background knowledge caveat those notes though.
         - If the context does not seem relevant to the answer say as such.
         </instructions>
         """),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])

stuff_documents_chain = create_stuff_documents_chain(chat, prompt_template)

retrieval_chain = create_retrieval_chain(retriever_chain, stuff_documents_chain)

# COMMAND ----------

user_question = "Can i bring my 80kg dog onboard?"

response = retrieval_chain.invoke({"chat_history": [], 
                              "input": user_question, 
                              "context": "",
                              "system_role":system_role})
display_chat('',response)

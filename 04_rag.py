# Databricks notebook source
# MAGIC %run ./utils/model_utils

# COMMAND ----------

# MAGIC %run ./00_customer_init

# COMMAND ----------


rag_context = RagContext(user_questions, contexts, system_roles, system_instructions)


# COMMAND ----------

# base_url = spark.conf.get("spark.base_url")
# sitemap_url = spark.conf.get("spark.sitemap_url")
db_catalog = spark.conf.get("spark.catalog")
db_schema = spark.conf.get("spark.schema")
db_table = spark.conf.get("spark.table")
vs_endpoint = spark.conf.get("spark.vs_endpoint")
embedding_endpoint_name = spark.conf.get("spark.embedding_endpoint_name")
vs_index = spark.conf.get("spark.vs_index")
vs_index_fullname = spark.conf.get("spark.vs_index_fullname")

# COMMAND ----------

## SET WHICH MODEL TO USE
# llama, mixtral, dbrx
model = dbrx

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

# COMMAND ----------

print("Questions")
print(rag_context.user_questions)

print("System Instructions")
print(rag_context.system_instructions)
print("System Role")
print(rag_context.system_roles)
print("Context")
print(rag_context.contexts)



# COMMAND ----------

# call_llm_with_context
# 1 : Question
# 2 : Context
# 3 : System Role
# 4 : System Instruction
# See 00_customer_init for configured Values
response1 = call_llm_with_context(retrieval_chain,rag_context, 0, 0, 0, 0)
display_chat('',response1)

# COMMAND ----------



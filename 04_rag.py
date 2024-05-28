# Databricks notebook source
# MAGIC %run ./utils/model_utils

# COMMAND ----------

# MAGIC %run ./00_customer_init

# COMMAND ----------


rag_context = RagContext(user_questions, contexts, system_roles, system_instructions)


# COMMAND ----------

# base_url = spark.conf.get("spark.base_url")
# sitemap_url = spark.conf.get("spark.sitemap_url")
db_catalog = spark.conf.get("spark.db_catalog")
db_schema = spark.conf.get("spark.db_schema")
db_table = spark.conf.get("spark.db_table")
vs_endpoint = spark.conf.get("spark.vs_endpoint")
embedding_endpoint_name = spark.conf.get("spark.embedding_endpoint_name")
vs_index = spark.conf.get("spark.vs_index")
vs_index_fullname = spark.conf.get("spark.vs_index_fullname")

# COMMAND ----------

## SET WHICH MODEL TO USE
# llama, mixtral, dbrx, # temp: mix8_pt, mix7_pt
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
#response1 = call_llm_with_context(retrieval_chain,rag_context, 5, 0, 2, 0)
display_chat('',response1)

# COMMAND ----------

response2 = call_llm_with_context(retrieval_chain,rag_context, 1, 0, 0, 0)
display_chat('',response2)

# COMMAND ----------

response3 = call_llm_with_context(retrieval_chain,rag_context, 2, 0, 0, 0)
display_chat('',response3)

# COMMAND ----------

response4 = call_llm_with_context(retrieval_chain,rag_context, 3, 0, 0, 0)
display_chat('',response4)

# COMMAND ----------

response5 = call_llm_with_context(retrieval_chain,rag_context, 4, 0, 0, 0)
display_chat('',response5)

# COMMAND ----------

response6 = call_llm_with_context(retrieval_chain,rag_context, 5, 0, 0, 0)
display_chat('',response6)

# COMMAND ----------

response7 = call_llm_with_context(retrieval_chain,rag_context, 6, 0, 0, 0)
display_chat('',response7)

# COMMAND ----------

for i in range(20):
  display_chat('',call_llm_with_context(retrieval_chain,rag_context, i, 0, 0, 1))

# COMMAND ----------



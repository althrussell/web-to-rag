# Databricks notebook source
# MAGIC %run ./utils/model_utils

# COMMAND ----------

## SET WHICH MODEL TO USE
# llama, mixtral, dbrx
model = mixtral

# COMMAND ----------

# MAGIC %run ./utils/00_setup

# COMMAND ----------

prompt = "As a camping and outdoor expert. Whats the best family tent for 4 people?"

# COMMAND ----------

# DBTITLE 1,Prompt Engineering
output = chat.invoke([HumanMessage(content=prompt)], max_tokens=500)

display_basic_chat(prompt,output.content)

# COMMAND ----------

# DBTITLE 1,RAG
display_chat('',call_llm_with_text(retrieval_chain,rag_context, user_question=prompt, context_index=0, system_role_index=3, system_instruction_index=2))

# COMMAND ----------



# Databricks notebook source
# MAGIC %pip install -U mlflow==2.13.0 llama_index langchain langchain-community

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %run ./utils/model_utils

# COMMAND ----------

llama = Model("llama", "databricks-meta-llama-3-70b-instruct","databricks",0.1)
mixtral = Model("mixtral", "databricks-mixtral-8x7b-instruct","databricks",0.1)
dbrx = Model("dbrx", "databricks-dbrx-instruct","databricks",0.1)



## SET WHICH MODEL TO USE
model = llama

# COMMAND ----------

print(Questions.get_questions("general_knowledge"))

# COMMAND ----------

# We will use the Langchain wrapper
pipe = ChatDatabricks(
    target_uri = model.target_uri,
    endpoint = model.endpoint,
    temperature = model.temperature
)



# COMMAND ----------

# MAGIC %md
# MAGIC # Prompting Techniques

# COMMAND ----------

# MAGIC %md
# MAGIC # Basic Prompting
# MAGIC Getting started is easy, we can send text in.
# MAGIC Remember that different models will respond differently!
# MAGIC The same model can also responds differently when we rerun a prompt
# MAGIC (though you likely only see this with basic one line prompts)

# COMMAND ----------

question_catagory = "general_knowledge" #Options are general_knowledge, programming, history, science_and_technology, literature
question_numer = 0
prompt = Questions.get_questions("general_knowledge")[question_numer]
print(f"Question Asked: {prompt}\n")

output = pipe.invoke([HumanMessage(content=prompt)], max_tokens=100)
print(f"Response: \n{output.content}")

# COMMAND ----------

# MAGIC %md
# MAGIC # Zero Shot Prompting
# MAGIC Zero shot is the most basic way to ask something of the model.
# MAGIC Just define your task and ask!

# COMMAND ----------

question_catagory = "general_knowledge" #Options are general_knowledge, programming, history, science_and_technology, literature
question_numer = 0
question = Questions.get_questions("general_knowledge")[question_numer]

prompt = f"""
    Summarise the question into the following categories general_knowledge, programming, history, science_and_technology, literature.
    Text: {question}
    Category:
"""

output = pipe.invoke([HumanMessage(content=prompt)], max_tokens=100)
str_output = print(output.content)

# COMMAND ----------



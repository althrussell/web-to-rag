# Databricks notebook source
# MAGIC %run ./utils/model_utils

# COMMAND ----------



## SET WHICH MODEL TO USE
# llama, mixtral, dbrx
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

# MAGIC %md
# MAGIC # Few Shot Prompting
# MAGIC One way to help the a model do logic better is to provide it with samples
# MAGIC
# MAGIC

# COMMAND ----------

prompt = """
<s>[INST]<<SYS>>
Be helpful and suggest a type of account for a customer.
<</SYS>>    

Here are some examples:
A consumer wants a savings account
A business wants a business account
A tech unicorn deserves a special VC account

Question:
What account would you recommend a small business?[/INST]
"""

output = pipe.invoke([HumanMessage(content=prompt)], max_tokens=100)
str_output = print(output.content)

# COMMAND ----------

# MAGIC %md
# MAGIC # System Prompts
# MAGIC Systems prompts can be used to instruct a model and also to tune it's reponse
# MAGIC You have already seen them. It is the bit inside the <<SYS>> tags.
# MAGIC They can have a big effect!
# MAGIC

# COMMAND ----------

system_prompt = 'Be helpful and suggest a type of account for a customer. try to be curteous and explain some of the key things to consider in bank account selection.'

user_question = 'I am a young student what account should I get?'

prompt = f"""
<s>[INST]<<SYS>>
{system_prompt}
<</SYS>>    

Here are some examples:
A consumer wants a savings account
A business wants a business account
A tech unicorn deserves a special VC account

Question:
{user_question}[/INST]
"""

output = pipe.invoke([HumanMessage(content=prompt)], max_tokens=100)
str_output = print(output.content)

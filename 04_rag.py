# Databricks notebook source
# MAGIC %run ./utils/model_utils

# COMMAND ----------

## SET WHICH MODEL TO USE
# llama, mixtral, dbrx, 
model = llama

# COMMAND ----------

# MAGIC %run ./utils/00_setup

# COMMAND ----------

# DBTITLE 1,Test Retreival Chain
print("Query 1: What measures does Rio Tinto take to protect biodiversity?")
result = retrieve_document_chain.invoke(
    {"messages": [{"role": "user", "content": "What measures does Rio Tinto take to protect biodiversity?"}]})
print(result)

# COMMAND ----------


display_chat('',call_llm_with_context(retrieval_chain,rag_context, user_question_index=0, context_index=0, system_role_index=0, system_instruction_index=2))

# COMMAND ----------

for i in range(10):
  display_chat('',call_llm_with_context(retrieval_chain,rag_context, user_question_index=i, context_index=0, system_role_index=0, system_instruction_index=2))

# COMMAND ----------

import mlflow
import pandas as pd
sample_questions = pd.DataFrame(
    user_questions, columns = ['eval_questions']
)

def eval_pipe(inputs):
    answers = []
    for index, row in inputs.iterrows():
        answer = retrieval_chain.invoke({"chat_history": [], 
                              "input": row.item(), 
                              "context": "","system_instruction":"","system_role":""})
        answers.append(answer['answer'])
    
    return answers


# COMMAND ----------


with mlflow.start_run(run_name='rio_gen_ai_basic_rag'):
  results = mlflow.evaluate(eval_pipe, 
                          data=sample_questions[0:20], 
                          model_type='text')

# COMMAND ----------



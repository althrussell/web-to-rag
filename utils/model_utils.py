# Databricks notebook source
from langchain_community.chat_models import ChatDatabricks
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


class Model:
    def __init__(self, name, endpoint, target_uri, temperature):
        self.name = name
        self.endpoint = endpoint
        self.target_uri = target_uri
        self.temperature = temperature


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

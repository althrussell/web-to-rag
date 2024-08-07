# Customer-Specific Demo for Web Scraping and Vector Search

This project demonstrates a customer-specific implementation for web scraping and vector search using Databricks. The workflow includes defining parameters, scraping web data, indexing it for vector search, and running a retrieval-augmented generation (RAG) model.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Usage](#usage)
  - [Step 00: Initialize Customer Demo](#step-00-initialize-customer-demo)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

This project is designed to showcase how to scrape web data, store it in Delta tables, and perform vector search using Databricks. The project also includes a retrieval-augmented generation (RAG) model to answer user questions based on the scraped data.

## Features

- Web scraping with configurable depth and chunk size
- Storing scraped data in Delta tables
- Creating and managing vector search indices
- Configurable RAG model for answering user questions

## Usage
Step 00: Initialize Customer Demo
```# Initialize for Specific Customer Demo

# Step 1: Define parameters
base_url = ""  # Replace with the URL you want to scrape
sitemap_url = "" # Replace with the sitemap URL if available, otherwise use None

# Unity Catalog Details
catalog = "shared"  # Replace with your catalog name
schema = "va_gen_ai_demo"  # Replace with your schema name
table = "web_scraper_data"  # Replace with your desired table name

# Vector Search Details
vs_endpoint = "dbdemos_vs_endpoint"
embedding_endpoint_name = "databricks-bge-large-en"

vs_index = f"{table}_bge_index"
vs_index_fullname = f"{catalog}.{schema}.{vs_index}"
```

Step01: Set Corporate colours and logo
```Change the below settings in utils/model_utils.py
# COMMAND ----------

bannerColor = '#cd2c2cff'
chatboxColor = '#efefefff'

imgurl = 'https://cdn.dataweavers.io/-/media/logo.svg'
```

# Define Questions and Roles
```
user_questions = [
    "Can I bring my 80kg dog onboard?",
    "What are the baggage restrictions for international flights?"
]

contexts = [
    "",
    "International flights often have stricter baggage policies."
]

system_roles = [
    "You are an experienced travel agent that takes a conversation between a traveller and yourself and answer their questions based on the below context.",
    "You are a knowledgeable customer service representative with expertise in airline policies."
]

system_instructions = [
    """- Do not answer saying 'Based on the context provided'
         - If there is a context provided. Focus your answers based on the context but provide additional helpful notes from your background knowledge caveat those notes though.
         - If there is no context use question and source data to answer.
         - If the context does not seem relevant to the answer say as such.""",
    "Provide a concise answer."
]
```

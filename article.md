# A simple RAG on crawled data
combining crawl4AI , supabase and n8n

## **Retrieval-Augmented Generation (RAG) - A brief overview**

Retrieval-Augmented Generation (RAG) is a powerful technique that combines the generative strength of large language models (LLMs) with the precision of retrieval-based systems. Instead of relying solely on a model’s internal knowledge, RAG pipelines dynamically pull in relevant external data—like documents, websites, or databases—at query time. This dramatically improves the factual accuracy and adaptability of LLMs, especially in domain-specific or frequently updated contexts.

At its core, a RAG workflow retrieves contextually relevant chunks of information using semantic search (typically via vector embeddings), then passes this context along with the user’s question into an LLM. The result is a grounded, contextualized answer that’s both coherent and informed by up-to-date data. Whether you're building an internal knowledge assistant or a public-facing chatbot, RAG helps ensure your AI is informed, not just intelligent.


# ingredients....
## n8n
[**n8n**](https://n8n.io/) is an open-source, low-code workflow automation tool that allows you to connect APIs, services, and custom logic with ease. It provides a visual interface where users can build complex automation pipelines by simply dragging and dropping nodes. With native support for hundreds of integrations and the ability to run JavaScript code or call webhooks, n8n is a powerful platform for orchestrating data flows—perfect for building Retrieval-Augmented Generation (RAG) applications that combine scraping, embedding, storage, and AI querying into a seamless process. You can either use the hosted version or self-host wherever you like. Sign-up and start automating 


## supabase 
[**Supabase**](https://supabase.com/) is an open-source backend-as-a-service that offers a powerful alternative to Firebase, built on top of PostgreSQL. It provides a fully managed database, real-time subscriptions, authentication, storage, and RESTful or GraphQL APIs out of the box. With a developer-friendly interface and tight integration with modern toolchains, Supabase is ideal for hosting and querying embedded data in RAG applications, enabling fast, scalable, and secure data access.

## Crawl4AI
[**Crawl4AI**](https://docs.crawl4ai.com/) is a lightweight, open-source web crawling framework designed specifically for AI and machine learning use cases. It simplifies the process of extracting structured content from websites, making it easy to gather high-quality text data for tasks like training models or building RAG pipelines. With built-in support for filtering, rate limiting, and customizable parsing logic, Crawl4AI is ideal for developers looking to integrate clean, domain-specific data into LLM workflows.


## LLaMA and ollama
[**LLaMA (Large Language Model Meta AI)**](https://www.llama.com/) is a family of open-source large language models developed by Meta, designed to provide high performance while being more resource-efficient than many other models in the same class. LLaMA models have been widely adopted in the AI community for their accessibility, strong multilingual capabilities, and ease of fine-tuning on domain-specific tasks. They are particularly well-suited for building local, privacy-respecting applications such as RAG (retrieval-augmented generation) systems, chatbots, and summarizers—especially when low-latency inference is required without relying on external APIs.

[**Ollama**](https://ollama.com/) is a developer-friendly tool that simplifies the deployment and management of LLaMA and other open-source language models via Docker containers (see [git-repo](https://github.com/ollama/ollama) and [docker-hub](https://hub.docker.com/r/ollama/ollama)). It abstracts away the complexity of setting up inference servers by offering a clean interface to run models locally with just a few commands. With Ollama, you can easily load, switch, and interact with LLaMA models using HTTP endpoints—making it an excellent choice for embedding models into workflows like n8n or integrating with data pipelines hosted on platforms like Supabase. This streamlined setup allows developers to run powerful LLMs on their own infrastructure, reducing dependencies on cloud-based services and improving control over cost and data privacy.

## Digital Ocean
[**DigitalOcean**](https://www.digitalocean.com/) is a cloud infrastructure provider known for its simplicity and developer-friendly tools. It offers scalable virtual machines (droplets), managed databases, and Kubernetes clusters, making it a popular choice for hosting applications, including LLM inference servers like Ollama, for around 20$ per month. We'll be making use of the option to deploy a docker file from your GitHub repository.


## Prerequisites
- n8n account
- supabase: Sign up and start a new project
- digital ocean account


## supabase init
The SQL script below sets up the foundational schema for using Supabase as a vector database to support RAG. 
First, it enables the `pgvector` extension, which allows for storing and querying high-dimensional vectors—essential for working with embeddings from language models. It then creates two tables: `crawled_pages`, which stores raw and processed data from web crawls (including HTML, markdown, and metadata), and `documents`, which holds the actual vectorized content used for semantic search, along with metadata and embeddings of dimension 768. We set the dimension to 768 because we will be using the [nomic-embed-text](https://ollama.com/library/nomic-embed-text) model for creating our embeddings.

The script also defines a custom SQL function, `match_documents`, which performs a vector similarity search using the `<=>` operator to compute cosine distance between the query embedding and stored document embeddings. It supports optional filtering based on JSON metadata and returns the most similar documents sorted by relevance. This function enables efficient retrieval of contextually relevant content for use in our RAG pipeline.


```sql
-- Enable the pgvector extension to work with embedding vectors
create extension vector;

-- Create a table to store page dats
drop table if exists crawled_pages;
create table crawled_pages (
  url text,
  created_at TIMESTAMP DEFAULT NOW(),
  links jsonb,
  metadata jsonb,
  markdown text,
  html text,
  cleaned_html text
);


-- Create a table to store your documents
drop table if exists documents;
create table documents (
  id bigserial primary key,
  content text, -- corresponds to Document.pageContent
  metadata jsonb, -- corresponds to Document.metadata
  embedding vector(768) -- 768 is the dimension of the embedding
);

-- Create a function to search for documents
create function match_documents (
  query_embedding vector(768),
  match_count int default null,
  filter jsonb DEFAULT '{}'
) returns table (
  id uuid,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
#variable_conflict use_column
begin
  return query
  select
    id,
    content,
    metadata,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where metadata @> filter
  order by documents.embedding <=> query_embedding
  limit match_count;
end;
$$;
```
To run the script open the `SQl Editor` in your Supabase project, paste the code and click `RUN`.
![supabase_init](pictures/supabase_init.png)

## crawl4ai code 

The repo is structured in the following:
```
├── requirements.txt
├── src
    ├── embed.py
    ├── main.py
    └── sb.py
```
Next we will setup the code for the crawl.

#### **`sb.py`**
```python 
import os
from supabase import create_client, Client

def get_client()-> Client:
    """
    This function creates a Supabase client using the URL and key from environment variables.
    """
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    return create_client(url, key)
```

- Llama on digital ocean 
- N8n workflow 
- First results
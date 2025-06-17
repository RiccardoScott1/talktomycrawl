# ---- GENERAL COMMENTS: ----

* the intro could be more punchy by highlighting / emphasising that this is not
just a RAG but a tool to turn any web-domain into a conversational DB
  * this would make it distinguishable from all the other RAG stuff
  * especially useful for the aforementioned non-tech audiences
* could be made more reader friendly with a few tweaks
  * long code blocks could be broken-up with the text explanations
  * a short abstract of building steps could be added
  * the end result should be shown (i.e. a conversation with the crawled data)
    * this could also be shown at the very beginning, so even people who do not
    intend to read fully can see its effect
* I would go as far as cutting most technical details which are not directly
related to setting up the vector DB and the infrastructure on `n8n`.

# ---- COMMENT END ----

# Chat with a web domain.....
combining crawl4AI , supabase and n8n

# ---- COMMENT: add the punchy intro about chat-w/-domain here ----

## **Retrieval-Augmented Generation (RAG) - A brief overview**

**Retrieval-Augmented Generation (RAG)** is an advanced approach that makes AI smarter and more reliable by combining two strengths: the creativity of language models and the accuracy of real-world information. Instead of depending only on what the AI already "knows," RAG helps it look up relevant facts—like searching through documents, websites, or databases—right when you ask a question.

Here's how it works: when you ask something, the system first finds pieces of information related to your question. Then, it gives that information to the AI, which uses it to write a more accurate, clear, and up-to-date response.

This means that whether you're building a helpful assistant for your team or a customer-facing chatbot, RAG helps ensure your AI gives answers that are not just well-written—but actually grounded in real, current knowledge.


# ---- COMMENT ----

I'd keep only one of the below (could split for article types): either the
short bulletpoints list or the more detailed subtitles listing, but not both.
Or, in the long technical article, have the bullet points and move the longer
descriptions to where the tools are being used with code / examples. That would
be good for signposting.
# ---- COMMENT END ----


## The services and tech needed to crawl a website and chat with the content
We'll briefly cover the various parts of our RAG prototype made of:
- a python repo to run [**Crawl4AI**](https://docs.crawl4ai.com/) locally and embed the documents using a
local ollama container
- a [**Supabase**](https://supabase.com/) database to hold the data (hosted by supabase so n8n can
access it remotely)
- [**n8n**](https://n8n.io/) to create a workflow with a chat and AI agent functionality
- a [**Ollama**](https://ollama.com/) service deployed on [**DigitalOcean**](https://www.digitalocean.com/) (so n8n can access it
remotely)


### n8n
[**n8n**](https://n8n.io/) is an open-source, low-code workflow automation tool
that allows you to connect APIs, services, and custom logic with ease. It
provides a visual interface where users can build complex automation pipelines
by simply dragging and dropping nodes. With native support for hundreds of
integrations and the ability to run JavaScript code or call webhooks, n8n is a
powerful platform for orchestrating data flows—perfect for building
Retrieval-Augmented Generation (RAG) applications that combine scraping,
embedding, storage, and AI querying into a seamless process. You can either use
the hosted version or self-host wherever you like. Sign-up and start automating.



### Supabase 
[**Supabase**](https://supabase.com/) is an open-source backend-as-a-service
that offers a powerful alternative to Firebase, built on top of PostgreSQL. It
provides a fully managed database, real-time subscriptions, authentication,
storage, and RESTful or GraphQL APIs out of the box. With a developer-friendly
interface and tight integration with modern toolchains, Supabase is ideal for
hosting and querying embedded data in RAG applications, enabling fast,
scalable, and secure data access.

### Crawl4AI
[**Crawl4AI**](https://docs.crawl4ai.com/) is a lightweight, open-source web
crawling framework designed specifically for AI and machine learning use cases.
It simplifies the process of extracting structured content from websites,
making it easy to gather high-quality text data for tasks like training models
or building RAG pipelines. With built-in support for filtering, rate limiting,
and customizable parsing logic, Crawl4AI is ideal for developers looking to
integrate clean, domain-specific data into LLM workflows.


### LLaMA and ollama
[**LLaMA (Large Language Model Meta AI)**](https://www.llama.com/) is a family
of open-source large language models developed by Meta, designed to provide
high performance while being more resource-efficient than many other models in
the same class. LLaMA models have been widely adopted in the AI community for 
their accessibility, strong multilingual capabilities, and ease of fine-tuning 
on domain-specific tasks. They are particularly well-suited for building local,
privacy-respecting applications such as RAG (retrieval-augmented generation)
systems, chatbots, and summarizers—especially when low-latency inference is 
required without relying on external APIs.

[**Ollama**](https://ollama.com/) is a developer-friendly tool that simplifies 
the deployment and management of LLaMA and other open-source language models
via Docker containers (see [git-repo](https://github.com/ollama/ollama) and 
[docker-hub](https://hub.docker.com/r/ollama/ollama)). It abstracts away the
complexity of setting up inference servers by offering a clean interface to run 
models locally with just a few commands. With Ollama, you can easily load, 
switch, and interact with LLaMA models using HTTP endpoints—making it an
excellent choice for embedding models into workflows like n8n or integrating
with data pipelines hosted on platforms like Supabase. This streamlined setup
allows developers to run powerful LLMs on their own infrastructure, reducing 
dependencies on cloud-based services and improving control over cost and data
privacy.

### Digital Ocean
[**DigitalOcean**](https://www.digitalocean.com/) is a cloud infrastructure 
provider known for its simplicity and developer-friendly tools. It offers 
scalable virtual machines (droplets), managed databases, and Kubernetes 
clusters, making it a popular choice for hosting applications, including LLM 
inference servers like Ollama, for around 20$ per month. We'll be making use
of the option to deploy a docker file from your GitHub repository.


## Implementation

# ---- COMMENT: add the implementation steps here ----

### Pre-requisites
- [n8n](https://n8n.io/) account
- Supabase: [Sign up](https://supabase.com/) and start a new project
- [Digital Ocean](https://www.digitalocean.com/) account
- OpenAi account and API key


# ---- COMMENT: i restructured this bit ----

### Supabase init
We start with a SQL file that sets up the foundational schema for using
Supabase as a vector database to support RAG. 
First, we enable the `pgvector` extension, which allows for storing and 
querying high-dimensional vectors—essential for working with embeddings from 
language models. We then create two tables. One, `crawled_pages`, which stores
raw and processed data from web crawls (including HTML, markdown, and
metadata), the second one, `documents`, which holds the actual vectorized 
content used for semantic search, along with metadata and embeddings of 
dimension 768. 

We set the dimension to 768 because we will be using the
[nomic-embed-text](https://ollama.com/library/nomic-embed-text) model for 
creating our embeddings.

The script is found in the detailed Supabase article (LINK TO SUPABASE ARTICLE)

#### **`main.py`**
The `main.py` script orchestrates the full web crawling and document embedding
pipeline using `crawl4ai`, Supabase, and a local embedding model. It 
asynchronously crawls a target website (e.g., `https://nexergroup.com`) using 
a configurable browser and deep crawl strategy, extracts and cleans HTML 
content, and processes the results. 

Successful crawls are stored in a Supabase table `crawled_pages` and passed 
through a document embedding function for vectorization (see `embed.py` later).
The setup enables automated content ingestion, transformation, and storage for
RAG applications.

# ---- COMMENT ----
I'd break up the main and make text comments inbetween. Maybe could have an
abstract level main first and then walk through its steps, although that could
be potentially confusing. I'd also keep code to minimum, so the browser /
crawler arguments could go (save for most essential i.e. strategy). We (ah...I)
should do a writeup on crawling and would be best to link it there to learn
more about specific settings
# ---- COMMENT END ----


#### **Embeddings**
# ---- COMMENT START -----
example of an embedding , 
add exapmle texts and chunks from one page???
# ---- COMMENT END -----

part of `process_result()` ... The `embed_documents` function in `embed.py`, processes and stores crawled web
content into our Supabase vector database: 
- cleaned HTML produced by Crawl4AI 
- splits it into semantically meaningful chunks using HTML headers
- embeds each chunk using the `nomic-embed-text` model via Ollama




These embeddings, along with associated metadata, are stored in the Supabase
`documents` table using LangChain’s `SupabaseVectorStore`. This setup enables
efficient semantic search and retrieval, which is crucial for building RAG
applications.



We will have one row per page in `crawled_pages` with useful extracted data
such internal and external urls, text, html and other metadata (for example:
title, author, some crawl specific data:depth (crawl depth), parent-url as well
as [Open Graph data](https://ogp.me/) ).

The `documents` table will hold several rows per page, one for each chunk that
got embedded.



### Ollama on digital ocean
Let's walk through the steps to deploy an app on Digital Ocean from a 
dockerfile on GitHub. 

#### A simple Ollama Dockerfile
Create a repo with the following Dockerfile:
```Dockerfile
# Start from the official Ollama image as the builder stage
FROM ollama/ollama:latest AS builder

# Define a build-time argument for the model name, allowing it to be passed when building the image
ARG MODEL_NAME_ENV
# Set an environment variable with a default model if none is provided
ENV MODEL_NAME=${MODEL_NAME_ENV:-nomic-embed-text}

# Start the Ollama server in the background, wait a bit for it to initialize,
# then pull the specified model so it's available in the final image
RUN ollama serve & \
    sleep 3 && \
    ollama pull ${MODEL_NAME}

# Use a fresh Ollama image for the final stage to keep it clean and minimal
FROM ollama/ollama:latest

# Copy the downloaded model data from the builder stage to this image
COPY --from=builder /root/.ollama /root/.ollama  

# Set the default command to start the Ollama server when the container runs
CMD ["serve"]
```

This Dockerfile sets up a minimal Ollama-based container for serving an LLM 
model, using a two-stage build to preload the specified model (defaulting to 
[`nomic-embed-text`](https://ollama.com/library/nomic-embed-text) in our case) 
and copy it into a clean runtime image. 

While it's well-suited for development or prototyping, **it should not be used 
in production environments** as it lacks essential security configurations such
as authentication, encrypted communication (TLS), and resource restrictions. 

Ollama doesn’t support setting API Key. The Ollama team recommends using a 
reverse proxy. Here's a 
[good article](https://medium.com/@qdrddr/ollama-with-apikey-litellm-proxy-c675c32ce7e8) 
on a workaround. 

We'll keep it simple here and just deploy our dockerfile on Digital Ocean.

#### Deploy the Dockerfile on Digital Ocean
In [Digital Ocean](https://www.digitalocean.com/) log into your account and:
- create a project
- click `create`>`App Platform`
- connect to your GitHub account
- select the repo with the Dockerfile you want to deploy

![digital_ocean_app](pictures/digital_ocean_app.png)


The default setting is 2 containers on 1GB RAM (2 x 12$ per month at the time
of writing). We picked **1 container on a 2GB RAM** instance (it costs almost 
the same: 25$ per month) to give it a bit more RAM. 

The default public port is **8080**, ollama is serving on **port 11434**, so
we set that as the Public HTTP port of our app.

After clicking `Create app` you'll have access to the URL, copy it for when
setting up your n8n workflow.

Every time you push changes to your repo Digital Ocean will re-build and
re-deploy.


### The n8n RAG workflow
The n8n workflow is straightforward, a chat node, an AI Agent connected to
OpenAi Chat Model (set up with your credentials), simple memory and the 
Supabase Vector Store tool using Ollama Embeddings.

![n8n_workflow](pictures/n8n_workflow.png)

Selecting and connecting the nodes is the easy part and done in a second. We'll 
now walk through configuring them.

#### Setting up the Supabase Vector Store node

![n8n_settings_supabase_vectorstore](pictures/n8n_settings_supabase_vectorstore.png)

To set up the Supabase Vector Store node you need 
- to provide `SUPABASE_URL` as `Host` and `SUPABASE_KEY` as 
`Service Role Secret` in the `Credential to connect with...` sub-menu 
- write a good description for your agent to understand when and how to use the 
vectorstore tool
- select the `documents` table that holds the embeddings

>**NOTE**: The default SQL function that will be called to find documents is `match_documents`, which is why we initialized and defined it in Supabase earlier.

#### Setting up Ollama embeddings
By default n8n's `Embeddings Ollama` node is set to send requests to an Ollama
service running on `localhost`. Since we are using a remote `n8n` instance,
we don't need have a localhost and we'll configure the node to send requests to
our Ollama app hosted on Digital Ocean.

![n8n_settings_ollama](pictures/n8n_settings_ollama.png)

For configuring:
- set the model to the same one used to create the embeddings (and the one
pulled to the Ollama app).
- click the edit button of `Credential to connect with` 
- set the Base URL with the URL from your Digital Ocean app.

![n8n_settings_ollama_account](pictures/n8n_settings_ollama_account.png)


## Run the crawl 
Last step is setting up the cralwer environment and we are ready to run the
crawl and start chatting with your data.

### install python virtual environment
```bash
python -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
```

### set up Crawl4AI
This will 
- install required Playwright browsers (Chromium, Firefox, etc.)
- perform OS-level checks (e.g., missing libs on Linux)
- confirm your environment is ready to crawl
```bash
source .venv/bin/activate 
crawl4ai-setup
```

### Get Ollama running locally 
For embedding locally we'll just start a local Ollama instance and pull `nomic-embed-text model`. You could also let langchain point to the app on Digital Ocean. 

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker exec -it ollama ollama pull nomic-embed-text
```

To test `ollama` is working locally the following command:

```bash
curl http://localhost:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "The sky is blue because of Rayleigh scattering"
}'
```

should return a json with embedding:
```json
{"embedding":[0.5897541046142578,...,0.48047590]}
```

### Crawl and Embed

To start the crawl, run the following from the root directory:
```bash
source .venv/bin/activate 
python src/main.py
```

## First results
If you open your Supabase project you should start seeing the `crawled_pages` 
as well as the `documents` tables being populated. 

Go over to your n8n workflow, open the chat of the chat node and should be able
to ask questions and get answers!


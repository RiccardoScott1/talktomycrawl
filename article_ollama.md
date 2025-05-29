# Deploy Ollama remotely on Digital Ocean
an **Ollama** service deployed on **Digital Ocean** (so n8n can access it remotely)

## Introduction
# ---- COMMENT START ----
write an introduction that motivates the need to use an ollama model served within your cloud infrastructure as opposed to using API calls to services like OpenAI/google and anthropic
# ---- COMMENT END ----


## LLaMA and ollama
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

## Digital Ocean
[**DigitalOcean**](https://www.digitalocean.com/) is a cloud infrastructure 
provider known for its simplicity and developer-friendly tools. It offers 
scalable virtual machines (droplets), managed databases, and Kubernetes 
clusters, making it a popular choice for hosting applications, including LLM 
inference servers like Ollama, for around 20$ per month. We'll be making use
of the option to deploy a docker file from your GitHub repository.


## Implementation

Let's walk through the steps to deploy an app on Digital Ocean from a 
dockerfile on GitHub. 

### Pre-requisites
- [Digital Ocean](https://www.digitalocean.com/) account
- github account


### A simple Ollama Dockerfile
Create a repo on GitHub with the following `Dockerfile`:
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

>**NOTE**: While it's well-suited for development or prototyping, **it should not be used 
in production environments** as it lacks essential security configurations such
as authentication, encrypted communication (TLS), and resource restrictions. 

# ---- COMMENT START ----
NOTE ask CORUN if this could actually still work 'safely' within a VPN....
# ---- COMMENT END ----


Ollama doesn’t support setting an API Key. The Ollama team recommends using a 
reverse proxy. Here's a 
[good article](https://medium.com/@qdrddr/ollama-with-apikey-litellm-proxy-c675c32ce7e8) 
on a workaround. 

We'll keep it simple and deploy our dockerfile on Digital Ocean.

### Deploy the Dockerfile on Digital Ocean
In [Digital Ocean](https://www.digitalocean.com/) log into your account and:
- create a project
- click `create`>`App Platform`
- connect to your `GitHub` account
- select the repo with the Dockerfile you want to deploy

![digital_ocean_app](pictures/digital_ocean_app.png)


The default setting is 2 containers on 1GB RAM (2 x 12$ per month at the time
of writing). We picked **1 container on a 2GB RAM** instance (it costs almost 
the same: 25$ per month) to give it a bit more RAM. 

The default public port is **8080**, ollama is serving on **port 11434**, so
we set that as the Public HTTP port of our app.

After clicking `Create app` you'll have access to the URL, 
copy it for sending requests to ollama or setting up your n8n workflow.

The best part: Every time you push changes to your repo Digital Ocean will re-build and
re-deploy.


## conclusion


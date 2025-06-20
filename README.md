# talktomycrawl

For main article on how to set up a domain based RAG with Crawl4ai, supabase, ollama and n8n see [here](https://riccardoscott1.github.io/articles/RAG-on-a-Web-Domain/Quickstart).

For indepth article on crawler see [here](https://riccardoscott1.github.io/articles/RAG-on-a-Web-Domain/Crawl4AI-domain-crawler).


## Prerequisites
Init Supabase, run `supabase_init.sql` on your supabase DB to create tables and functions. See [here](https://riccardoscott1.github.io/articles/RAG-on-a-Web-Domain/N8N-and-Supabase) for details. 

Local Docker installation.


### Install Python Virtual Environment
In the root directory of the repo run:
```bash
python -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
```

### Set up Crawl4AI
This will 
- install required Playwright browsers (Chromium, Firefox, etc.)
- perform OS-level checks (e.g., missing libs on Linux)
- confirm your environment is ready to crawl
```bash
source .venv/bin/activate 
crawl4ai-setup
```


>**Note**: Alternatively 
>```bash
>make install
>```
>will run all install Python Virtual Environment and setup Crawl4AI.


## Start a local Ollama Instance and Pull Model

Start up Ollama and pull the embedding model: `nomic-embed-text model`

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker exec -it ollama ollama pull nomic-embed-text
```
 
## Test Ollama is Working
Running
```bash
curl http://localhost:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "The sky is blue because of Rayleigh scattering"
}'
```

should return a json with the embedding:
```json
{"embedding":[0.5897541046142578,...,-0.48047590]}
```

## Populate .env file
See .env.example for what's needed.

## install env
```bash
make install
```


## Crawl and Embed
To start the crawl, run the following from the root directory:
```bash
source .venv/bin/activate 
python src/main.py
```

or short:

```bash
make run
```





# resources
https://thoughtbot.com/blog/how-to-use-open-source-LLM-model-locally

model
https://ollama.com/library/nomic-embed-text



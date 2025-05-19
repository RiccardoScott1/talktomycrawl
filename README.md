# talktomycrawl

Article on how to set up a simple RAG with Crawl4ai, supabase, ollama and n8n.
See article.md . 



init suapbase , run supabase_init.sql on your supabase DB to create tables and functions


## Start a local Ollama instance and pull `nomic-embed-text model`

- start up ollama
- pull the model
```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker exec -it ollama ollama pull nomic-embed-text
```
 
## test ollama is working
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

## populate .env file
see .env.example for what's needed.

## install env
```bash
make install
```

## run crawler
```bash
make run
```





# resources
https://thoughtbot.com/blog/how-to-use-open-source-LLM-model-locally

model
https://ollama.com/library/nomic-embed-text




curl http://178.128.35.162:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "The sky is blue because of Rayleigh scattering"
}'


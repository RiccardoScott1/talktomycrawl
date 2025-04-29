# talktomycrawl

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker exec -it ollama ollama run nomic-embed-text
```



https://thoughtbot.com/blog/how-to-use-open-source-LLM-model-locally

model
https://ollama.com/library/nomic-embed-text

your_digital_ocean_ip_address


curl http://localhost:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "The sky is blue because of Rayleigh scattering"
}'

curl http://178.128.35.162:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "The sky is blue because of Rayleigh scattering"
}'


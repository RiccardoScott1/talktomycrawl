include .env
.PHONY: install

install:
	rm -rf .venv
	python -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	(source .venv/bin/activate && crawl4ai-setup)

run:
	(source .venv/bin/activate && python src/main.py)
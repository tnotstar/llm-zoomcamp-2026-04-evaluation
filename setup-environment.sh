#!/usr/bin/bash

echo "Setting up Python environment..."
python -m pip install -U pip

echo "Setting up UV environment..."
pipx install uv

echo "Initializing project..."
uv init --no-workspace
uv add openai pydantic python-dotenv pandas
uv add onnxruntime tokenizers numpy tqdm minsearch gitsource

echo "Jupyter & IPython kernel will be installed by the Antigravity IDE..."
echo "(Omiting Jupyter Notebook installation)"
# uv add jupyterlab
# uv add ipykernel

echo "Download helper modules..."
PREFIX=https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/main
wget -N ${PREFIX}/01-agentic-rag/code/ingest.py
wget -N ${PREFIX}/01-agentic-rag/code/rag_helper.py
wget -N ${PREFIX}/02-vector-search/embed/download.py
wget -N ${PREFIX}/02-vector-search/embed/embedder.py
wget -N ${PREFIX}/04-evaluation/code/evaluation_utils.py

echo "Downloading models..."
uv run python download.py

echo "NB: Use .env file for API keys"

exit 0

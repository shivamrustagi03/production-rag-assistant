# Production RAG Assistant

A production-style Retrieval-Augmented Generation system for question answering over PDFs and text documents. The project is designed as a realistic AI Engineer portfolio project: modular enough to explain in interviews, simple enough to run locally, and grounded in practical RAG engineering choices.

## Project Overview

This repository converts a tutorial RAG pipeline into a clean application with document ingestion, chunking, sentence-transformer embeddings, FAISS vector search, prompt-managed generation, source citations, a Streamlit chat UI, lightweight evaluation, tests, and Docker support.

## Problem Statement

Large language models can hallucinate when answering from memory. This project reduces that risk by retrieving relevant chunks from user-provided documents and using those chunks as grounded context before generating an answer.

## Architecture Diagram

```text
PDF/TXT documents
      |
      v
Document Loader -> Preprocessing -> Text Chunking
      |
      v
SentenceTransformer Embeddings
      |
      v
FAISS Vector Store (persistent)
      |
      v
Retriever -> Prompt Builder -> Groq LLM
      |
      v
Answer + Source References
```

## Features

- Ingest PDF and text documents from `data/raw`
- Chunk documents with configurable chunk size and overlap
- Generate embeddings using `all-MiniLM-L6-v2`
- Persist and reload FAISS vector indexes
- Retrieve top-k relevant chunks with source/page metadata
- Generate grounded answers using Groq when `GROQ_API_KEY` is configured
- Fall back to extractive answers when no API key is available
- Streamlit frontend with document upload, chat, loading indicators, and sources
- Lightweight evaluation script for sample queries
- Minimal tests for chunking and retrieval behavior
- Dockerfile for local containerized execution

## Tech Stack

- Python 3.11+
- LangChain document loaders and text splitters
- Sentence Transformers
- FAISS
- Groq LLM API
- Streamlit
- PyYAML and python-dotenv
- Pytest

## Folder Structure

```text
production-rag-assistant/
├── app/
│   ├── core/              # Config and constants
│   ├── generation/        # LLM client, prompt builder, response generation
│   ├── ingestion/         # Loading, preprocessing, chunking
│   ├── retrieval/         # Embeddings, FAISS store, retriever
│   └── utils/             # Logging and helpers
├── configs/
│   └── config.yaml
├── data/
│   ├── raw/               # Source PDFs/text files
│   ├── processed/         # Optional processed artifacts
│   └── vector_db/         # Local FAISS indexes
├── evaluation/
│   └── basic_eval.py
├── experiments/
│   └── notebooks/
├── frontend/
│   └── streamlit_app.py
├── prompts/
│   └── rag_prompt.txt
├── tests/
├── Dockerfile
├── main.py
└── requirements.txt
```

## Setup Instructions

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Add your Groq API key to `.env`:

```text
GROQ_API_KEY=your_groq_api_key_here
```

The project can run without the key, but it will return an extractive fallback answer instead of an LLM-generated answer.

## How To Run

Build the vector index:

```bash
python main.py ingest
```

Ask a question:

```bash
python main.py ask "What is machine learning?"
```

Launch the Streamlit app:

```bash
streamlit run frontend/streamlit_app.py
```

Run tests:

```bash
pytest
```

Run with Docker:

```bash
docker build -t production-rag-assistant .
docker run -p 8501:8501 --env-file .env production-rag-assistant
```

## How RAG Works

1. Documents are loaded from `data/raw`.
2. Text is cleaned and split into overlapping chunks.
3. Each chunk is embedded with a sentence-transformer model.
4. Embeddings and metadata are stored in a persistent FAISS index.
5. User questions are embedded and searched against FAISS.
6. Retrieved chunks are inserted into a prompt template.
7. The LLM generates an answer grounded in the retrieved context.
8. The response includes source references from document metadata.

## Example Workflow

1. Place PDFs or `.txt` files in `data/raw`, or upload them in Streamlit.
2. Run ingestion to build the vector database.
3. Ask a document-specific question.
4. Review the answer and cited sources.
5. Tune `configs/config.yaml` for chunking and retrieval behavior.

## Example Queries

- What is Python used for?
- Explain supervised learning.
- What is the attention mechanism?
- Summarize the key points from the uploaded report.

## Screenshots

Add screenshots after running the app:

- `screenshots/streamlit-chat.png`
- `screenshots/source-citations.png`
- `screenshots/upload-flow.png`

## Skills Demonstrated

- End-to-end RAG system design
- Document ingestion and preprocessing
- Embedding model integration
- Vector database persistence
- Retrieval orchestration
- Prompt management
- LLM integration with environment-based secrets
- Source-grounded generation
- Streamlit application development
- Testing and lightweight evaluation
- Docker-based packaging

## Resume Value

This project demonstrates the ability to take a notebook/tutorial-style GenAI pipeline and turn it into a maintainable application. It shows practical AI Engineering skills across retrieval, embeddings, vector stores, prompt design, UI integration, evaluation, and deployment readiness.

## Future Improvements

- Add hybrid retrieval with BM25 plus vector search
- Add reranking for improved answer quality
- Store evaluation runs as JSON or CSV
- Add FastAPI for serving the RAG pipeline as an API
- Add authentication and per-user document indexes
- Add observability with structured traces and latency metrics


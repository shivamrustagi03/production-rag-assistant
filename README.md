# 🚀 Production-Style Multi-Document RAG Assistant

A modular Retrieval-Augmented Generation (RAG) system for document-grounded question answering using **FAISS, SentenceTransformers, Groq LLMs, and Streamlit**.

Designed as a production-style AI Engineering project showcasing modular architecture, configurable pipelines, persistent retrieval, source-grounded responses, Docker support, testing, and evaluation.

## 📌 Project Overview

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline that retrieves relevant document chunks before generating answers.

Users can upload **PDF and text documents**, ask questions in natural language, and receive **context-grounded responses with source references**.

### Key Goals

* Reduce hallucinations through retrieval-grounded generation
* Enable question answering over custom documents
* Demonstrate production-oriented GenAI system design
* Showcase AI Engineering best practices

## 🏗️ Architecture

```text
Documents (PDF/TXT)
        ↓
Document Loading
        ↓
Preprocessing
        ↓
Recursive Chunking
        ↓
SentenceTransformer Embeddings
        ↓
FAISS Vector Database
        ↓
User Query
        ↓
Top-K Retrieval (k=4)
        ↓
Prompt Assembly
        ↓
Groq LLM (gemma2-9b-it)
        ↓
Grounded Response + Sources
```

## ✨ Features

### Core Features

* Multi-document retrieval (PDF + TXT)
* Persistent FAISS vector database
* Configurable chunking and retrieval
* Source-grounded answers
* Prompt externalization
* Modular architecture

### Frontend

* Streamlit chat interface
* Multi-file upload
* Session history
* Loading indicators
* Source references

### Engineering

* Docker support
* `.env` management
* YAML configs
* Logging
* Evaluation module
* Unit tests

## 🧠 Tech Stack

| Category         | Technology            |
| ---------------- | --------------------- |
| Language         | Python                |
| LLM              | Groq (`gemma2-9b-it`) |
| Embeddings       | `all-MiniLM-L6-v2`    |
| Vector DB        | FAISS                 |
| Frontend         | Streamlit             |
| Frameworks       | LangChain             |
| Testing          | Pytest                |
| Config           | YAML + dotenv         |
| Containerization | Docker                |

## 📂 Project Structure

```text
production-rag-assistant/
├── app/
├── configs/
├── data/
├── evaluation/
├── experiments/
├── frontend/
├── prompts/
├── tests/
├── Dockerfile
├── README.md
└── main.py
```

## ⚙️ Run Locally

```bash
git clone https://github.com/shivamrustagi03/production-rag-assistant.git
cd production-rag-assistant
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env`

```env
GROQ_API_KEY=your_api_key
```

Run Streamlit:

```bash
streamlit run frontend/streamlit_app.py
```

## 🐳 Docker

```bash
docker build -t production-rag-assistant .
docker run -p 8501:8501 production-rag-assistant
```

## 🧪 Testing

```bash
pytest
```

Current coverage:

* Retrieval pipeline
* Chunking logic

## 📊 Evaluation

Includes a lightweight evaluation pipeline for:

* Retrieved chunks
* Source inspection
* Answer previews

Future metrics:

* Precision@K
* Faithfulness
* Groundedness
* Answer relevancy

## 📸 Screenshots

Add screenshots for:

* Streamlit UI
* Document upload flow
* Source-grounded responses

## 💼 Skills Demonstrated

* Retrieval-Augmented Generation (RAG)
* Vector Databases (FAISS)
* Embedding Models
* Prompt Engineering
* Streamlit Frontend
* Modular Software Design
* Dockerization
* Testing & Evaluation
* Production-Oriented AI Engineering

## 🎯 Resume Positioning

**Production-Style Multi-Document RAG Assistant**

Built a modular Retrieval-Augmented Generation system for document-grounded QA using SentenceTransformers, FAISS, Groq, and Streamlit with persistent retrieval, prompt-managed generation, Docker support, and testing.

## 🧠 Interview Talking Points

* Why FAISS for vector search
* Why recursive chunking
* Config-driven architecture
* External prompt management
* Tradeoffs of dense retrieval

## 🚀 Future Improvements

* FastAPI backend
* Hybrid retrieval
* Reranking
* Metadata filtering
* Streaming responses
* Better evaluation metrics
* CI/CD
* Observability

# Production RAG Repository Audit

==================================================
1. PROJECT SUMMARY
==================================================

Project Name: `production-rag-assistant`

One-line description: A production-style multi-document RAG assistant with FAISS retrieval, Groq generation, Streamlit UI, and lightweight evaluation.

Main goal of the project: Build a modular Retrieval-Augmented Generation pipeline for answering questions over local PDF and text documents.

What problem does it solve? It grounds LLM answers in retrieved document chunks to reduce unsupported answers when asking questions over custom documents.

Who is the target user? A local user or AI Engineer portfolio reviewer who wants to ingest PDFs/text files and ask document-grounded questions through a CLI or Streamlit UI.

==================================================
2. TECH STACK
==================================================

Programming language: Python.

Frameworks used: LangChain document loaders/text splitters, Streamlit, pytest.

LLM used: Groq via `langchain_groq.ChatGroq`; configured model is `gemma2-9b-it`.

Embedding model used: `all-MiniLM-L6-v2` via `sentence-transformers`.

Vector database: FAISS using `faiss.IndexFlatIP`.

Frontend framework: Streamlit.

Backend/API: Not implemented. The project has a CLI entrypoint in `main.py`, but no FastAPI/Flask/API server.

Libraries/frameworks: `faiss-cpu`, `langchain`, `langchain-community`, `langchain-core`, `langchain-groq`, `langchain-text-splitters`, `numpy`, `pypdf`, `python-dotenv`, `pyyaml`, `sentence-transformers`, `streamlit`, `pytest`.

Package manager: `pip` with `requirements.txt`; `pyproject.toml` also exists. `uv.lock` and a zero-byte `uv` file exist in the repository.

Environment management: `.python-version` specifies `3.11`; `.env.example` exists; a local `.venv` exists but is ignored by `.gitignore`.

Containerization: Dockerfile is implemented.

Deployment readiness: Basic containerized Streamlit deployment readiness exists via Dockerfile. Production hosting, authentication, monitoring, and API deployment are not implemented.

==================================================
3. RAG ARCHITECTURE
==================================================

Full RAG pipeline:

Document files in `data/raw`
↓
Document loading with `PyPDFLoader` and `TextLoader`
↓
Text cleanup with `clean_text`
↓
Recursive character chunking
↓
SentenceTransformer embeddings
↓
FAISS index build and persistence
↓
User query
↓
Query embedding
↓
FAISS vector retrieval
↓
Context assembly with numbered source blocks
↓
Prompt template from `prompts/rag_prompt.txt`
↓
Groq LLM generation
↓
Answer plus source references

Retrieval strategy: Dense vector retrieval over embedded chunks.

Similarity search type: Inner product search with `faiss.IndexFlatIP` after L2 normalization of vectors, effectively cosine-style similarity.

top_k value: `4` in `configs/config.yaml`.

Chunking strategy: `RecursiveCharacterTextSplitter` with separators `["\n\n", "\n", " ", ""]`.

Chunk size: `900` in `configs/config.yaml`.

Overlap: `150` in `configs/config.yaml`.

Prompt strategy: Prompt is externalized in `prompts/rag_prompt.txt`; retrieved chunks are formatted as numbered context blocks with source labels.

Persistence method: FAISS index is saved to `faiss.index`; chunk text and metadata are pickled to `metadata.pkl` under the configured vector DB directory.

Metadata usage: Stores LangChain document metadata, adds `source` and `chunk_id`, preserves PDF page metadata when provided by `PyPDFLoader`, and formats sources as filename or filename plus page number.

==================================================
4. DOCUMENT PROCESSING
==================================================

Supported file types: `.pdf` and `.txt`.

How documents are loaded: `load_documents` recursively scans the configured data directory and uses `PyPDFLoader` for PDFs and `TextLoader` with UTF-8 encoding for text files.

How chunking is done: Loaded `Document` objects are passed to `split_documents`.

Chunking method: LangChain `RecursiveCharacterTextSplitter`.

Chunk size: `900` from config; function default is `1000`.

Overlap: `150` from config; function default is `200`.

Preprocessing steps: Removes null characters, collapses spaces/tabs, reduces three or more newlines to two newlines, and strips leading/trailing whitespace.

Metadata stored: `source`, `chunk_id`, and any metadata provided by the original loader, including PDF page metadata when available.

How vector storage works: Chunk texts are embedded, normalized, added to a FAISS `IndexFlatIP`, and persisted with metadata/text payload using pickle.

==================================================
5. FRONTEND FEATURES
==================================================

Implemented frontend features:

- Streamlit page titled `Production RAG Assistant`
- Sidebar section named `Knowledge Base`
- Multi-file upload for PDF and text files
- Uploaded files saved to `data/raw/uploads`
- `Ingest documents` button
- Rebuilds retriever/vector store after upload
- `Load existing index` button
- Chat input using `st.chat_input`
- Chat message rendering using `st.chat_message`
- Session-based message history through `st.session_state.messages`
- Session-based retriever caching through `st.session_state.retriever`
- Loading spinner during document indexing
- Loading spinner during retrieval and answer generation
- Source references displayed with `st.caption`
- Multi-document support through multiple uploaded files and recursive document loading

Streaming response: Not implemented.

Clear chat: Not implemented.

Frontend error handling: Not implemented explicitly; exceptions are not caught in `frontend/streamlit_app.py`.

==================================================
6. CONFIGURATION SYSTEM
==================================================

Is `config.yaml` implemented? Yes.

Configurable parameters:

- `data.raw_dir`
- `data.processed_dir`
- `data.vector_db_dir`
- `ingestion.chunk_size`
- `ingestion.chunk_overlap`
- `embedding.model_name`
- `retrieval.top_k`
- `generation.provider`
- `generation.model_name`
- `generation.temperature`

Is `.env` used? Yes. `load_dotenv()` is called in `GroqLLM`.

Which environment variables are needed? `GROQ_API_KEY`.

Is prompt modularized? Yes. The prompt lives in `prompts/rag_prompt.txt`.

==================================================
7. EVALUATION SYSTEM
==================================================

What evaluation exists? `evaluation/basic_eval.py` defines `evaluate_queries`.

What metrics are measured? No formal metrics are measured. It returns query, number of retrieved chunks, sources, and a 300-character answer preview.

How evaluation works? It loads config, builds/loads a retriever, creates a `ResponseGenerator`, runs each query, retrieves chunks, generates an answer, and stores a small result dictionary.

Benchmarking present? Not implemented.

Test dataset present? Not implemented. The script contains three hardcoded sample queries.

==================================================
8. TESTING
==================================================

What tests exist?

- `tests/test_chunking.py`
- `tests/test_retrieval.py`

What modules are tested?

- `app.ingestion.text_splitter.split_documents`
- `app.retrieval.vector_store.FaissVectorStore`

Are tests functional? Yes. Running `.venv\Scripts\python.exe -m pytest` collected 2 tests and reported `2 passed`. In the current Windows environment, pytest also printed a post-summary access-violation traceback involving installed packages.

Coverage level: Basic.

==================================================
9. PRODUCTION FEATURES
==================================================

Logging: Implemented through `app/utils/logger.py` using Python `logging`.

Error handling: Partially implemented. Document loading catches per-file exceptions, vector store validates missing indexes/empty chunks, and response generation catches LLM errors and returns an extractive fallback. Frontend-level error handling is not implemented.

Type hints: Implemented across most application functions/classes.

Docker: Implemented with a Streamlit Dockerfile.

Persistent vector DB: Implemented with FAISS index file plus pickle metadata/text payload.

Modular architecture: Implemented with `app/core`, `app/ingestion`, `app/retrieval`, `app/generation`, and `app/utils`.

Prompt management: Implemented with `prompts/rag_prompt.txt`.

Config-driven architecture: Implemented with `configs/config.yaml` and `AppConfig`.

Caching: Partially implemented in Streamlit session state for messages and retriever. No persistent application cache is implemented.

Retry mechanisms: Not implemented.

API endpoints: Not implemented.

Monitoring/observability: Not implemented beyond standard logging.

==================================================
10. FOLDER STRUCTURE
==================================================

```text
multi-document-rag-pipeline/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── constants.py
│   ├── generation/
│   │   ├── __init__.py
│   │   ├── llm.py
│   │   ├── prompt_builder.py
│   │   └── response_generator.py
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── document_loader.py
│   │   ├── preprocessing.py
│   │   └── text_splitter.py
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   ├── search.py
│   │   └── vector_store.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── helpers.py
│   │   └── logger.py
│   └── __init__.py
├── configs/
│   └── config.yaml
├── data/
│   ├── processed/
│   ├── raw/
│   │   ├── pdf/
│   │   │   ├── PatternPDF.pdf
│   │   │   └── Project Report 51 New.pdf
│   │   ├── text_files/
│   │   │   ├── machine_learning.txt
│   │   │   └── python_intro.txt
│   │   └── uploads/
│   └── vector_db/
├── evaluation/
│   └── basic_eval.py
├── experiments/
│   └── notebooks/
│       ├── 1-langchain-document-components.svg
│       ├── document.ipynb
│       └── pdf_loader.ipynb
├── frontend/
│   └── streamlit_app.py
├── prompts/
│   └── rag_prompt.txt
├── tests/
│   ├── test_chunking.py
│   └── test_retrieval.py
├── .env.example
├── .gitignore
├── .python-version
├── Dockerfile
├── README.md
├── main.py
├── pyproject.toml
├── requirements.txt
├── run_streamlit.bat
├── uv
└── uv.lock
```

==================================================
11. KEY FEATURES
==================================================

- Modular RAG architecture
- Config-driven pipeline
- PDF and text document ingestion
- Recursive text chunking
- SentenceTransformer embeddings
- Persistent FAISS vector database
- Dense vector retrieval
- Prompt template stored outside code
- Groq LLM integration through environment variable
- Extractive fallback when LLM generation is unavailable
- Source references in generated response payload and Streamlit UI
- Streamlit chat interface
- Upload and ingest documents from the frontend
- CLI commands for ingestion and question answering
- Lightweight evaluation script
- Basic pytest coverage
- Dockerfile for Streamlit execution

==================================================
12. ADVANCED FEATURES
==================================================

Hybrid retrieval: Not implemented.

Reranking: Not implemented.

Metadata filtering: Not implemented.

Multi-document retrieval: Implemented. Documents are loaded recursively and all chunks are indexed in one FAISS store.

Context compression: Not implemented.

Citation generation: Partially implemented. The prompt instructs the LLM to mention source numbers, and the app returns/displays source references, but there is no citation verification system.

Query reformulation: Not implemented.

Agentic behavior: Not implemented.

==================================================
13. LIMITATIONS
==================================================

- No backend API endpoints.
- No authentication or user management.
- No formal evaluation metrics such as retrieval precision, faithfulness, answer relevancy, or groundedness.
- No benchmark dataset.
- No hybrid retrieval or reranking.
- No metadata filtering.
- No streaming LLM response in Streamlit.
- No clear-chat button in the frontend.
- No frontend try/except error handling.
- No retry logic for LLM/API failures.
- No monitoring or tracing beyond standard logs.
- No production database for document/index metadata.
- FAISS metadata persistence uses pickle, which is simple but not ideal for untrusted data or multi-user production systems.
- Current vector DB directory exists but no persisted FAISS files were found during this audit.
- The project has both `requirements.txt` and `pyproject.toml`; dependency management is not fully unified.
- `uv.lock` exists, but the project primarily documents pip/requirements usage.

What would improve this to production-grade AI Engineer level?

- Add FastAPI endpoints for ingestion, retrieval, and answer generation.
- Add structured evaluation with a small labeled QA dataset.
- Add reranking and optional hybrid retrieval.
- Add metadata filters by document, page, or file type.
- Add streaming responses and frontend error handling.
- Add structured logging, traces, and latency metrics.
- Replace pickle metadata storage with a safer structured format or database.
- Add CI workflow for tests and linting.

==================================================
14. RESUME POSITIONING
==================================================

Best project title: Production-Style Multi-Document RAG Assistant

Strong 2-line resume description:

Built a modular Retrieval-Augmented Generation system for question answering over PDFs and text files using SentenceTransformers, FAISS, Groq, and Streamlit. Implemented configurable ingestion, chunking, persistent vector search, prompt-managed generation, source references, Docker support, and basic testing/evaluation.

4 strong resume bullet points:

- Designed a modular RAG pipeline with separate ingestion, retrieval, generation, configuration, and utility layers.
- Implemented persistent FAISS-based dense retrieval using normalized SentenceTransformer embeddings and configurable top-k search.
- Built a Streamlit chat interface with PDF/text upload, document ingestion, session history, loading states, and source references.
- Added production-readiness components including config management, environment-based secrets, logging, Dockerfile, basic tests, and lightweight evaluation.

==================================================
15. INTERVIEW TALKING POINTS
==================================================

Architecture choices:

- The project separates ingestion, retrieval, generation, configuration, and UI into distinct modules.
- FAISS is used for local vector persistence and fast similarity search.
- Prompt text is stored outside application code for easier iteration.
- Config values are centralized in YAML instead of being hardcoded.

Tradeoffs:

- FAISS `IndexFlatIP` is simple and exact, but it is not optimized for very large-scale approximate search.
- Pickle metadata persistence is simple for a portfolio/local project, but it is not ideal for untrusted or multi-user production data.
- Groq integration provides hosted LLM generation, but the app depends on `GROQ_API_KEY` for real LLM output.
- The fallback answer keeps the app usable without an API key, but it is extractive rather than generative.

Engineering decisions:

- Recursive chunking is used to preserve paragraph/line/word boundaries where possible.
- Vectors are normalized before inner-product search to support cosine-style retrieval.
- Source metadata is preserved and displayed to make answers traceable.
- Streamlit session state stores chat history and the retriever for the current app session.

Scalability discussion:

- The current design is suitable for local multi-document QA and portfolio demonstration.
- For larger scale, the project would need approximate indexes, metadata filtering, API endpoints, background ingestion jobs, persistent metadata storage, and observability.

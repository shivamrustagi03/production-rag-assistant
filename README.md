# 🚀 Production-Style Multi-Document RAG Assistant

A modular Retrieval-Augmented Generation system for document-grounded question answering using **FAISS, SentenceTransformers, Groq LLMs, LangChain, and Streamlit**.

The system enables users to upload multiple documents, process them through an ingestion pipeline, store semantic representations, retrieve relevant information using vector similarity search, and generate grounded responses with source references.

---

# 📌 Project Overview

This project implements an end-to-end document question-answering system where users can interact with their own documents through a conversational interface.

The system follows a modular architecture separating:

- Document ingestion
- Text preprocessing
- Chunk creation
- Embedding generation
- Vector storage
- Retrieval
- Response generation

The objective is to build a production-style GenAI application with clear separation between retrieval and generation components.

---

# 🏗️ System Architecture

                     Documents
                   (PDF / TXT)
                        |
                        ↓
              Document Ingestion Layer
                        |
                        ↓
             Text Cleaning & Processing
                        |
                        ↓
             Recursive Text Chunking
                        |
                        ↓
          SentenceTransformer Embeddings
                        |
                        ↓
               FAISS Vector Index
                        |
                        |
                        |
                        ↓

                  User Query
                        |
                        ↓
            Query Embedding Generation
                        |
                        ↓
          Similarity Search using FAISS
                        |
                        ↓
             Top-K Relevant Chunks
                        |
                        ↓
             Prompt Construction
                        |
                        ↓
             Groq LLM (Gemma2-9B)
                        |
                        ↓
          Grounded Response + Sources

---

# 🔄 End-to-End Pipeline

## 1. Document Ingestion Pipeline

The ingestion pipeline is responsible for converting raw documents into a format that can be processed by the retrieval system.

Supported document types:

- PDF
- TXT


The pipeline performs:

- Document loading
- Text extraction
- Basic preprocessing
- Metadata preservation


The output of this stage is a collection of processed document objects that are passed to the chunking stage.

---

# 2. Document Chunking

Large documents are divided into smaller chunks before embedding generation.

The project uses:


RecursiveCharacterTextSplitter


Chunking is performed because the retrieval system works more effectively with smaller semantic units instead of entire documents.

The chunking process maintains:

- Configurable chunk size
- Chunk overlap
- Document metadata


Example flow:


Document

↓

Chunk 1
Chunk 2
Chunk 3

↓

Embedding Generation


The overlap between chunks helps preserve context between adjacent sections.

---

# 3. Embedding Generation

After documents are split into chunks, each chunk is converted into a numerical representation using an embedding model.

Embedding model used:


SentenceTransformer
(all-MiniLM-L6-v2)


The embedding pipeline converts:


Text Chunk

↓

Vector Representation


These vectors capture semantic information and allow similarity-based retrieval.

The same embedding model is used for:

1. Document indexing
2. User query conversion


---

# 4. Vector Storage Using FAISS

The project uses FAISS as the vector storage and similarity search engine.

FAISS is responsible for:

- Storing document embeddings
- Building the vector index
- Performing similarity search
- Retrieving relevant chunks


During ingestion:


Document Chunk

↓

Embedding Vector

↓

FAISS Index


During querying:


User Query

↓

Query Vector

↓

FAISS Similarity Search

↓

Relevant Documents


The vector index is persisted so that embeddings do not need to be regenerated every time the application starts.

---

# 5. Retrieval Pipeline

The retrieval layer connects user queries with stored document knowledge.

The retrieval process:


User Question

↓

Query Embedding

↓

Vector Similarity Search

↓

Top-K Relevant Chunks

↓

Context for LLM


The retriever is responsible for finding the most relevant document sections based on semantic similarity.

The retrieved context is then passed to the generation pipeline.

---

# 6. Prompt Construction and Generation

The generation layer combines:

- User query
- Retrieved document context
- System instructions

to create the final prompt.

Flow:


Retrieved Context

User Question

↓

Prompt Template

↓

Groq LLM

↓

Generated Response


The LLM used:


Groq - Gemma2-9B-IT


The response is generated using retrieved information instead of relying only on the model's internal knowledge.

---

# 📂 Project Structure


production-rag-assistant/

│
├── app/
│ │
│ ├── ingestion/
│ │ ├── document_loader.py
│ │ ├── preprocessing.py
│ │ └── text_splitter.py
│ │
│ ├── retrieval/
│ │ ├── embeddings.py
│ │ ├── vector_store.py
│ │ └── retriever.py
│ │
│ ├── generation/
│ │ ├── prompt_builder.py
│ │ ├── llm.py
│ │ └── response_generator.py
│ │
│ ├── core/
│ │ └── config.py
│
├── frontend/
│ └── streamlit_app.py
│
├── configs/
│
├── prompts/
│
├── evaluation/
│
├── tests/
│
├── main.py
│
├── Dockerfile
│
└── README.md


---

# 🧩 Core Components

## Document Loader

Responsible for:

- Reading uploaded files
- Extracting text
- Creating document objects
- Maintaining metadata


---

## Text Processing Module

Responsible for:

- Cleaning extracted content
- Preparing documents before chunking


---

## Chunking Module

Responsible for:

- Splitting documents into smaller units
- Maintaining overlap
- Preparing chunks for embedding generation


---

## Embedding Module

Responsible for:

- Loading the embedding model
- Converting text chunks into vectors
- Generating query embeddings


---

## Vector Store Module

Responsible for:

- Creating FAISS index
- Saving and loading embeddings
- Performing similarity search


---

## Retrieval Module

Responsible for:

- Query processing
- Retrieving relevant chunks
- Passing context to generation


---

## Generation Module

Responsible for:

- Building prompts
- Calling the LLM
- Formatting final responses


---

# ⚙️ Configuration Management

The project separates configuration from implementation logic.

Configuration handles:

- Model selection
- Chunking parameters
- Retrieval settings
- Paths
- Environment variables


The project uses:

- YAML configuration files
- `.env` variables


This keeps the system flexible and easier to modify.

---

# 🖥️ Application Flow

## Document Upload Flow


User uploads documents

↓

Streamlit interface receives files

↓

Documents are loaded

↓

Text is processed

↓

Chunks are created

↓

Embeddings are generated

↓

FAISS index is created


---

## Question Answering Flow


User enters question

↓

Query embedding generated

↓

FAISS searches similar vectors

↓

Relevant chunks retrieved

↓

Prompt is constructed

↓

Groq LLM generates response

↓

Answer displayed with sources


---

# 🛠️ Design Decisions

## Why FAISS?

FAISS was selected because:

- The project can run locally
- It provides efficient similarity search
- It avoids external infrastructure dependency


For larger production deployments, alternatives like Pinecone, Milvus, or Weaviate can be considered.

---

## Why SentenceTransformer?

The embedding model was selected because:

- It is open source
- It can run locally
- It provides efficient semantic embeddings


---

## Why Modular Architecture?

The project separates responsibilities into independent modules:

- Ingestion
- Retrieval
- Generation
- Frontend

This improves:

- Maintainability
- Testing
- Future scalability


---

# 🚀 Future Improvements

Potential improvements:

- Hybrid search (BM25 + vector retrieval)
- Metadata filtering
- Reranking models
- Streaming responses
- Better evaluation metrics
- FastAPI backend
- Observability using LangSmith
- CI/CD pipeline

---

# 🧪 Evaluation

The project includes evaluation support for analyzing:

- Retrieved document chunks
- Source relevance
- Generated responses


Future evaluation improvements:

- Faithfulness
- Context relevance
- Answer relevance
- Precision@K
- Recall@K

---

# 🛠️ Technologies Used

| Component | Technology |
|---|---|
| Language | Python |
| LLM | Groq Gemma2-9B |
| Embeddings | SentenceTransformers |
| Vector Store | FAISS |
| Framework | LangChain |
| Frontend | Streamlit |
| Testing | Pytest |
| Configuration | YAML + dotenv |
| Containerization | Docker |

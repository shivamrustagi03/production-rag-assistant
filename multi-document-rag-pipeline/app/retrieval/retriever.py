from langchain_core.documents import Document

from app.retrieval.embeddings import EmbeddingModel
from app.retrieval.vector_store import FaissVectorStore


class Retriever:
    def __init__(self, vector_store: FaissVectorStore, embedding_model: EmbeddingModel) -> None:
        self.vector_store = vector_store
        self.embedding_model = embedding_model

    def index_documents(self, chunks: list[Document]) -> None:
        embeddings = self.embedding_model.encode([chunk.page_content for chunk in chunks])
        self.vector_store.build(chunks, embeddings)
        self.vector_store.save()

    def retrieve(self, query: str, top_k: int) -> list[dict]:
        query_embedding = self.embedding_model.encode([query])
        return self.vector_store.search(query_embedding, top_k=top_k)


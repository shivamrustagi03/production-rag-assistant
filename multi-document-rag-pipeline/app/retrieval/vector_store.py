import pickle
from pathlib import Path
from typing import Any

import numpy as np
from langchain_core.documents import Document

from app.utils.helpers import ensure_directory
from app.utils.logger import get_logger

logger = get_logger(__name__)


class FaissVectorStore:
    def __init__(self, persist_dir: str | Path) -> None:
        self.persist_dir = ensure_directory(persist_dir)
        self.index: Any | None = None
        self.metadata: list[dict[str, Any]] = []
        self.texts: list[str] = []

    @property
    def index_path(self) -> Path:
        return self.persist_dir / "faiss.index"

    @property
    def metadata_path(self) -> Path:
        return self.persist_dir / "metadata.pkl"

    def exists(self) -> bool:
        return self.index_path.exists() and self.metadata_path.exists()

    def build(self, chunks: list[Document], embeddings: np.ndarray) -> None:
        if len(chunks) == 0:
            raise ValueError("Cannot build vector store with zero chunks.")

        vectors = self._normalize(embeddings)
        import faiss

        self.index = faiss.IndexFlatIP(vectors.shape[1])
        self.index.add(vectors)
        self.texts = [chunk.page_content for chunk in chunks]
        self.metadata = [dict(chunk.metadata) for chunk in chunks]
        logger.info("Built FAISS index with %s chunks", len(chunks))

    def save(self) -> None:
        if self.index is None:
            raise ValueError("No FAISS index available to save.")

        import faiss

        faiss.write_index(self.index, str(self.index_path))
        with self.metadata_path.open("wb") as file:
            pickle.dump({"metadata": self.metadata, "texts": self.texts}, file)
        logger.info("Saved vector store to %s", self.persist_dir)

    def load(self) -> None:
        if not self.exists():
            raise FileNotFoundError(f"Vector store not found in {self.persist_dir}")

        import faiss

        self.index = faiss.read_index(str(self.index_path))
        with self.metadata_path.open("rb") as file:
            payload = pickle.load(file)
        self.metadata = payload["metadata"]
        self.texts = payload["texts"]
        logger.info("Loaded vector store from %s", self.persist_dir)

    def search(self, query_embedding: np.ndarray, top_k: int) -> list[dict[str, Any]]:
        if self.index is None:
            raise ValueError("Vector store is not loaded.")

        query_vector = self._normalize(query_embedding)
        scores, indices = self.index.search(query_vector, top_k)
        results: list[dict[str, Any]] = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append(
                {
                    "score": float(score),
                    "text": self.texts[idx],
                    "metadata": self.metadata[idx],
                }
            )
        return results

    @staticmethod
    def _normalize(vectors: np.ndarray) -> np.ndarray:
        vectors = np.asarray(vectors, dtype="float32")
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1
        return vectors / norms

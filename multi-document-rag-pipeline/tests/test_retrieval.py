import numpy as np
from langchain_core.documents import Document

from app.retrieval.vector_store import FaissVectorStore


def test_vector_store_returns_highest_similarity(tmp_path) -> None:
    chunks = [
        Document(page_content="Python programming", metadata={"source": "python.txt"}),
        Document(page_content="Machine learning", metadata={"source": "ml.txt"}),
    ]
    embeddings = np.array([[1.0, 0.0], [0.0, 1.0]], dtype="float32")
    store = FaissVectorStore(tmp_path)

    store.build(chunks, embeddings)
    results = store.search(np.array([[0.9, 0.1]], dtype="float32"), top_k=1)

    assert results[0]["text"] == "Python programming"
    assert results[0]["metadata"]["source"] == "python.txt"

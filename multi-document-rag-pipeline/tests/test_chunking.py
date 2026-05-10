from langchain_core.documents import Document

from app.ingestion.text_splitter import split_documents


def test_split_documents_preserves_metadata() -> None:
    docs = [Document(page_content="Python is useful for AI. " * 60, metadata={"source": "python.txt"})]

    chunks = split_documents(docs, chunk_size=120, chunk_overlap=20)

    assert len(chunks) > 1
    assert chunks[0].metadata["source"] == "python.txt"
    assert chunks[0].metadata["chunk_id"] == 0


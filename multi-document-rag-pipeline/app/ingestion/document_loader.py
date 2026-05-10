from pathlib import Path

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader

from app.ingestion.preprocessing import clean_text
from app.utils.logger import get_logger

logger = get_logger(__name__)


def load_documents(data_dir: str | Path) -> list[Document]:
    data_path = Path(data_dir)
    if not data_path.exists():
        raise FileNotFoundError(f"Data directory not found: {data_path}")

    documents: list[Document] = []
    loaders = {
        ".pdf": lambda path: PyPDFLoader(str(path)),
        ".txt": lambda path: TextLoader(str(path), encoding="utf-8"),
    }

    for file_path in sorted(path for path in data_path.rglob("*") if path.is_file()):
        loader_factory = loaders.get(file_path.suffix.lower())
        if loader_factory is None:
            continue

        try:
            loaded_docs = loader_factory(file_path).load()
            for doc in loaded_docs:
                doc.page_content = clean_text(doc.page_content)
                doc.metadata["source"] = str(file_path)
            documents.extend(doc for doc in loaded_docs if doc.page_content)
            logger.info("Loaded %s documents from %s", len(loaded_docs), file_path.name)
        except Exception as exc:
            logger.warning("Failed to load %s: %s", file_path, exc)

    logger.info("Loaded %s total documents", len(documents))
    return documents


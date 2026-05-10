from app.core.config import AppConfig
from app.ingestion.document_loader import load_documents
from app.ingestion.text_splitter import split_documents
from app.retrieval.embeddings import EmbeddingModel
from app.retrieval.retriever import Retriever
from app.retrieval.vector_store import FaissVectorStore
from app.utils.logger import get_logger

logger = get_logger(__name__)


def build_retriever(config: AppConfig, rebuild: bool = False) -> Retriever:
    vector_store = FaissVectorStore(config.vector_db_dir)
    embedding_model = EmbeddingModel(config.embedding_model)
    retriever = Retriever(vector_store, embedding_model)

    if rebuild or not vector_store.exists():
        documents = load_documents(config.raw_data_dir)
        chunks = split_documents(documents, config.chunk_size, config.chunk_overlap)
        retriever.index_documents(chunks)
        logger.info("Indexed %s chunks", len(chunks))
    else:
        vector_store.load()

    return retriever


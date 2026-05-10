import numpy as np

from app.utils.logger import get_logger

logger = get_logger(__name__)


class EmbeddingModel:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            logger.info("Loading embedding model: %s", self.model_name)
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def encode(self, texts: list[str]) -> np.ndarray:
        embeddings = self.model.encode(texts, show_progress_bar=len(texts) > 8)
        return np.asarray(embeddings, dtype="float32")

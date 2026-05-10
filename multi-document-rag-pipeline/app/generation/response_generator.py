from app.core.config import AppConfig
from app.generation.llm import GroqLLM
from app.generation.prompt_builder import build_prompt
from app.utils.helpers import format_source
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ResponseGenerator:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self._llm: GroqLLM | None = None

    @property
    def llm(self) -> GroqLLM:
        if self._llm is None:
            self._llm = GroqLLM(self.config.llm_model, self.config.temperature)
        return self._llm

    def answer(self, query: str, retrieved_chunks: list[dict]) -> dict:
        if not retrieved_chunks:
            return {"answer": "No relevant document context was found.", "sources": []}

        sources = [format_source(chunk.get("metadata", {})) for chunk in retrieved_chunks]
        prompt = build_prompt(query, retrieved_chunks)

        try:
            answer = self.llm.generate(prompt)
        except Exception as exc:
            logger.warning("LLM generation unavailable, returning extractive fallback: %s", exc)
            answer = self._fallback_answer(query, retrieved_chunks)

        return {"answer": answer, "sources": list(dict.fromkeys(sources))}

    @staticmethod
    def _fallback_answer(query: str, retrieved_chunks: list[dict]) -> str:
        best_chunk = retrieved_chunks[0]
        source = format_source(best_chunk.get("metadata", {}))
        text = best_chunk.get("text", "").strip()
        preview = text[:900] + ("..." if len(text) > 900 else "")
        return (
            f"Based on the retrieved context for '{query}', the most relevant passage is from "
            f"{source}:\n\n{preview}"
        )


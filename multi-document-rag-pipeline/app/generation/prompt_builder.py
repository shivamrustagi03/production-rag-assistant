from pathlib import Path

from app.core.constants import DEFAULT_PROMPT_PATH
from app.utils.helpers import format_source


def build_context(retrieved_chunks: list[dict]) -> str:
    context_blocks = []
    for idx, chunk in enumerate(retrieved_chunks, start=1):
        source = format_source(chunk.get("metadata", {}))
        context_blocks.append(f"[{idx}] Source: {source}\n{chunk.get('text', '')}")
    return "\n\n".join(context_blocks)


def build_prompt(query: str, retrieved_chunks: list[dict], prompt_path: str | Path = DEFAULT_PROMPT_PATH) -> str:
    template = Path(prompt_path).read_text(encoding="utf-8")
    return template.format(query=query, context=build_context(retrieved_chunks))


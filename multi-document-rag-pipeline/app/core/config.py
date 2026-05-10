from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from app.core.constants import DEFAULT_CONFIG_PATH, PROJECT_ROOT


@dataclass(frozen=True)
class AppConfig:
    raw_data_dir: Path
    vector_db_dir: Path
    chunk_size: int
    chunk_overlap: int
    embedding_model: str
    retrieval_top_k: int
    llm_provider: str
    llm_model: str
    temperature: float


def _resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else PROJECT_ROOT / path


def load_config(config_path: str | Path = DEFAULT_CONFIG_PATH) -> AppConfig:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        data: dict[str, Any] = yaml.safe_load(file) or {}

    data_cfg = data.get("data", {})
    ingestion_cfg = data.get("ingestion", {})
    embedding_cfg = data.get("embedding", {})
    retrieval_cfg = data.get("retrieval", {})
    generation_cfg = data.get("generation", {})

    return AppConfig(
        raw_data_dir=_resolve_path(data_cfg.get("raw_dir", "data/raw")),
        vector_db_dir=_resolve_path(data_cfg.get("vector_db_dir", "data/vector_db/faiss")),
        chunk_size=int(ingestion_cfg.get("chunk_size", 1000)),
        chunk_overlap=int(ingestion_cfg.get("chunk_overlap", 200)),
        embedding_model=str(embedding_cfg.get("model_name", "all-MiniLM-L6-v2")),
        retrieval_top_k=int(retrieval_cfg.get("top_k", 4)),
        llm_provider=str(generation_cfg.get("provider", "groq")),
        llm_model=str(generation_cfg.get("model_name", "gemma2-9b-it")),
        temperature=float(generation_cfg.get("temperature", 0.2)),
    )


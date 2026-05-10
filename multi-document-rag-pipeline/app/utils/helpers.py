from pathlib import Path


def ensure_directory(path: str | Path) -> Path:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def format_source(metadata: dict) -> str:
    source = Path(str(metadata.get("source", "unknown"))).name
    page = metadata.get("page")
    return f"{source}, page {int(page) + 1}" if page is not None else source


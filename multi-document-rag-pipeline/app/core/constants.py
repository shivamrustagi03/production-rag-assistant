from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "config.yaml"
DEFAULT_PROMPT_PATH = PROJECT_ROOT / "prompts" / "rag_prompt.txt"


import argparse

from app.core.config import load_config
from app.generation.response_generator import ResponseGenerator
from app.retrieval.search import build_retriever
from app.utils.logger import get_logger

logger = get_logger(__name__)


def ingest(rebuild: bool = True) -> None:
    config = load_config()
    build_retriever(config, rebuild=rebuild)
    logger.info("Ingestion complete.")


def ask(query: str) -> None:
    config = load_config()
    retriever = build_retriever(config)
    chunks = retriever.retrieve(query, config.retrieval_top_k)
    response = ResponseGenerator(config).answer(query, chunks)

    print("\nAnswer:\n")
    print(response["answer"])
    if response["sources"]:
        print("\nSources:")
        for source in response["sources"]:
            print(f"- {source}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Production-style RAG pipeline")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("ingest", help="Build or rebuild the FAISS vector store")
    ask_parser = subparsers.add_parser("ask", help="Ask a question over indexed documents")
    ask_parser.add_argument("query", nargs="?", default="What is machine learning?")

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "ingest":
        ingest()
    elif args.command == "ask":
        ask(args.query)
    else:
        ingest(rebuild=False)
        ask("What is machine learning?")


if __name__ == "__main__":
    main()


from app.core.config import load_config
from app.generation.response_generator import ResponseGenerator
from app.retrieval.search import build_retriever


def evaluate_queries(queries: list[str]) -> list[dict]:
    config = load_config()
    retriever = build_retriever(config)
    generator = ResponseGenerator(config)
    rows = []

    for query in queries:
        chunks = retriever.retrieve(query, config.retrieval_top_k)
        response = generator.answer(query, chunks)
        rows.append(
            {
                "query": query,
                "retrieved_chunks": len(chunks),
                "sources": response["sources"],
                "answer_preview": response["answer"][:300],
            }
        )
    return rows


if __name__ == "__main__":
    sample_queries = [
        "What is Python used for?",
        "What is machine learning?",
        "What is attention mechanism?",
    ]
    for row in evaluate_queries(sample_queries):
        print(row)


from app.rag.embeddings import generate_embeddings
from app.workflows.state import RetrievedContextState


def retrieve_context(
    collection,
    query: str,
    top_k: int = 3
) -> list[RetrievedContextState]:

    query_embedding = generate_embeddings(
        [query]
    )[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    contexts: list[RetrievedContextState] = []

    for document, metadata in zip(
        documents,
        metadatas
    ):
        contexts.append(
            {
                "path": str(metadata["path"]),
                "symbol": str(metadata["symbol"]),
                "chunk_type": str(
                    metadata["chunk_type"]
                ),
                "content": document
            }
        )

    return contexts
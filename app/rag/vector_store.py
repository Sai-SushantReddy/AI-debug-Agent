import chromadb

from app.rag.embeddings import generate_embeddings
from app.workflows.state import RetrievedContextState


chroma_client = chromadb.Client()


def create_repository_collection(
    chunks: list[RetrievedContextState]
):
    collection = chroma_client.get_or_create_collection(
        name="debug_repository"
    )

    if not chunks:
        return collection

    ids = [
        f"chunk-{index}"
        for index in range(len(chunks))
    ]

    documents = [
        chunk["content"]
        for chunk in chunks
    ]

    metadatas = [
        {
            "path": chunk["path"],
            "symbol": chunk["symbol"],
            "chunk_type": chunk["chunk_type"]
        }
        for chunk in chunks
    ]

    embeddings = generate_embeddings(documents)

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    return collection
import pickle
from pathlib import Path

import chromadb
from fastembed import TextEmbedding


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHROMA_PATH = PROJECT_ROOT / "data" / "chroma"
BM25_PATH = PROJECT_ROOT / "data" / "bm25" / "index.pkl"


# --------------------------------------------------
# Configuration
# --------------------------------------------------

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
COLLECTION_NAME = "novacart_policies"

TOP_K = 3


# --------------------------------------------------
# Lazy Embedding Model
# --------------------------------------------------
embedding_model = None


def get_embedding_model():
    global embedding_model

    if embedding_model is None:
        print("Loading embedding model...")
        embedding_model = TextEmbedding(
            model_name=MODEL_NAME
        )

    return embedding_model


# --------------------------------------------------
# Connect to ChromaDB
# --------------------------------------------------

print("Connecting to ChromaDB...")

chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = chroma_client.get_collection(
    name=COLLECTION_NAME
)


# --------------------------------------------------
# Load BM25 index
# --------------------------------------------------

print("Loading BM25 index...")

with open(BM25_PATH, "rb") as file:
    bm25_data = pickle.load(file)

bm25 = bm25_data["bm25"]
bm25_chunks = bm25_data["chunks"]


# --------------------------------------------------
# Semantic Search
# --------------------------------------------------

def semantic_search(query, top_k=TOP_K):

    model = get_embedding_model()

    query_embedding = list(
    model.embed([query])
)[0]

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    results_list = []

    for i in range(len(results["documents"][0])):

        results_list.append({
            "content": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "chunk_id": results["metadatas"][0][i]["chunk_id"],
            "method": "semantic"
        })

    return results_list


# --------------------------------------------------
# BM25 Search
# --------------------------------------------------

def keyword_search(query, top_k=TOP_K):

    query_tokens = query.lower().split()

    scores = bm25.get_scores(query_tokens)

    ranked_indices = scores.argsort()[::-1][:top_k]

    results = []

    for index in ranked_indices:

        results.append({
            "content": bm25_chunks[index]["content"],
            "source": bm25_chunks[index]["source"],
            "chunk_id": bm25_chunks[index]["chunk_id"],
            "method": "keyword"
        })

    return results


# --------------------------------------------------
# Hybrid Search
# --------------------------------------------------

def hybrid_search(query, top_k=TOP_K):

    semantic_results = semantic_search(
        query,
        top_k
    )

    keyword_results = keyword_search(
        query,
        top_k
    )

    combined = {}

    # Add semantic results
    for result in semantic_results:

        combined[result["chunk_id"]] = result

    # Add keyword results
    for result in keyword_results:

        if result["chunk_id"] in combined:

            combined[result["chunk_id"]]["method"] = "hybrid"

        else:

            combined[result["chunk_id"]] = result

    return list(combined.values())[:top_k]


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    query = input("\nAsk NovaCart a question: ")

    results = hybrid_search(query)

    print("\nHYBRID SEARCH RESULTS")
    print("=" * 60)

    for i, result in enumerate(results, start=1):

        print(f"\nResult {i}")
        print(f"Source: {result['source']}")
        print(f"Method: {result['method']}")
        print(f"Chunk ID: {result['chunk_id']}")

        print("\nContent:")
        print(result["content"])

        print("-" * 60)
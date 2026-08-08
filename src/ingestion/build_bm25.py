import pickle
from pathlib import Path

from load_documents import load_documents
from chunk_documents import chunk_text


# --------------------------------------------------
# Configuration
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

BM25_DIR = PROJECT_ROOT / "data" / "bm25"
BM25_DIR.mkdir(parents=True, exist_ok=True)

BM25_PATH = BM25_DIR / "index.pkl"


# --------------------------------------------------
# Load BM25
# --------------------------------------------------

from rank_bm25 import BM25Okapi


# --------------------------------------------------
# Load and chunk documents
# --------------------------------------------------

documents = load_documents()

all_chunks = []

for document in documents:

    chunks = chunk_text(document["content"])

    for index, chunk in enumerate(chunks):

        all_chunks.append({
            "content": chunk,
            "source": document["source"],
            "chunk_id": f"{document['source']}_{index}"
        })


# --------------------------------------------------
# Tokenize chunks
# --------------------------------------------------

tokenized_chunks = [
    chunk["content"].lower().split()
    for chunk in all_chunks
]


# --------------------------------------------------
# Build BM25 index
# --------------------------------------------------

print(f"Building BM25 index for {len(all_chunks)} chunks...")

bm25 = BM25Okapi(tokenized_chunks)


# --------------------------------------------------
# Save index + chunks
# --------------------------------------------------

with open(BM25_PATH, "wb") as file:

    pickle.dump(
        {
            "bm25": bm25,
            "chunks": all_chunks
        },
        file
    )


# --------------------------------------------------
# Verify
# --------------------------------------------------

print("\nBM25 index created successfully!")

print(f"Chunks indexed: {len(all_chunks)}")

print(f"Saved to: {BM25_PATH}")
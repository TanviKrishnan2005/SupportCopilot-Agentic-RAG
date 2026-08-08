from sentence_transformers import SentenceTransformer

from chunk_documents import chunk_text
from load_documents import load_documents


# --------------------------------------------------
# Load embedding model
# --------------------------------------------------

MODEL_NAME = "all-MiniLM-L6-v2"

print(f"Loading embedding model: {MODEL_NAME}")

model = SentenceTransformer(MODEL_NAME)


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
# Generate embeddings
# --------------------------------------------------

texts = [chunk["content"] for chunk in all_chunks]

print(f"\nGenerating embeddings for {len(texts)} chunks...")

embeddings = model.encode(
    texts,
    show_progress_bar=True
)


# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\nEmbedding generation complete!")

print(f"Number of embeddings: {len(embeddings)}")
print(f"Embedding dimensions: {len(embeddings[0])}")

print("\nExample:")
print(f"Chunk ID: {all_chunks[0]['chunk_id']}")
print(f"Source: {all_chunks[0]['source']}")
print(f"Vector preview: {embeddings[0][:5]}")
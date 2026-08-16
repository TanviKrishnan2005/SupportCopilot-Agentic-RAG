import chromadb
from fastembed import TextEmbedding

from chunk_documents import chunk_text
from load_documents import load_documents


# --------------------------------------------------
# Configuration
# --------------------------------------------------

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

CHROMA_PATH = "data/chroma"

COLLECTION_NAME = "novacart_policies"


# --------------------------------------------------
# Load embedding model
# --------------------------------------------------

print("Loading embedding model...")

embedding_model = TextEmbedding(
    model_name=MODEL_NAME
)


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

print(f"Generating embeddings for {len(texts)} chunks...")

embeddings = list(
    embedding_model.embed(texts)
)


# --------------------------------------------------
# Create ChromaDB client
# --------------------------------------------------

print("\nCreating ChromaDB...")

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


# --------------------------------------------------
# Create collection
# --------------------------------------------------

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


# --------------------------------------------------
# Store chunks and embeddings
# --------------------------------------------------

collection.add(
    ids=[chunk["chunk_id"] for chunk in all_chunks],
    documents=texts,
    embeddings=[embedding.tolist() for embedding in embeddings],
    metadatas=[
        {
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"]
        }
        for chunk in all_chunks
    ]
)


# --------------------------------------------------
# Verify
# --------------------------------------------------

print("\nChromaDB ingestion complete!")

print(
    f"Documents stored: {collection.count()}"
)

print(
    f"Collection: {COLLECTION_NAME}"
)
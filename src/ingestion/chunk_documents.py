from pathlib import Path

from load_documents import load_documents


# --------------------------------------------------
# Configuration
# --------------------------------------------------

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


# --------------------------------------------------
# Chunking Function
# --------------------------------------------------

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Split text into overlapping chunks.

    Example:

    chunk 1: characters 0 - 500
    chunk 2: characters 400 - 900
    chunk 3: characters 800 - 1300

    The overlap helps preserve context between chunks.
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

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

    print(f"Documents loaded: {len(documents)}")
    print(f"Total chunks created: {len(all_chunks)}")

    print("\nSample chunks:\n")

    for chunk in all_chunks[:5]:

        print("-" * 60)
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(f"Source: {chunk['source']}")
        print(chunk["content"][:300])
        print("-" * 60)
from pathlib import Path


# Find project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Policy directory
POLICY_DIR = PROJECT_ROOT / "data" / "policies"


def load_documents():
    documents = []

    for file_path in sorted(POLICY_DIR.glob("*.md")):

        content = file_path.read_text(encoding="utf-8")

        documents.append({
            "content": content,
            "source": file_path.name
        })

    return documents


if __name__ == "__main__":

    documents = load_documents()

    print(f"Loaded {len(documents)} documents\n")

    for document in documents:

        print("-" * 50)
        print(f"Source: {document['source']}")
        print(f"Characters: {len(document['content'])}")
        print("-" * 50)
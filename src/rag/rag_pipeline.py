import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from hybrid_retriever import hybrid_search


# --------------------------------------------------
# Environment
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# LLM
# --------------------------------------------------

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


# --------------------------------------------------
# Generate RAG Answer
# --------------------------------------------------

def answer_question(question):

    # Retrieve relevant chunks
    results = hybrid_search(question, top_k=3)

    # Build context
    context_parts = []

    for result in results:

        context_parts.append(
            f"Source: {result['source']}\n"
            f"{result['content']}"
        )

    context = "\n\n---\n\n".join(context_parts)

    # Prompt
    prompt = f"""
You are NovaCart's customer support assistant.

Answer the customer's question using ONLY the provided
NovaCart policy information.

If the provided information does not contain the answer,
say that you do not have enough information and recommend
contacting NovaCart support.

Do not invent policies, prices, timelines, or rules.

Customer question:
{question}

Relevant NovaCart policy information:
{context}

Give a concise, helpful answer.

At the end, include:

Sources:
- <source filename>
"""

    # Generate answer
    response = llm.invoke(prompt)

    return response.content, results


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    question = input("\nAsk NovaCart a question: ")

    answer, results = answer_question(question)

    print("\n" + "=" * 60)
    print("NOVACART SUPPORT")
    print("=" * 60)

    print("\n" + answer)

    print("\nRetrieved sources:")

    for result in results:
        print(
            f"- {result['source']} "
            f"({result['method']})"
        )
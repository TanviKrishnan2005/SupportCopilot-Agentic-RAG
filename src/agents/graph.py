from langgraph.graph import StateGraph, START, END
from typing import TypedDict

from src.rag.rag_pipeline import answer_question


# --------------------------------------------------
# Agent State
# --------------------------------------------------

class AgentState(TypedDict):
    message: str
    response: str
    intent: str
    tool_result: dict
    context: list


# --------------------------------------------------
# RAG Node
# --------------------------------------------------

def rag_node(state: AgentState):

    question = state["message"]

    answer, results = answer_question(question)

    return {
        "response": answer,
        "context": results
    }


# --------------------------------------------------
# Build Graph
# --------------------------------------------------

graph_builder = StateGraph(AgentState)

graph_builder.add_node("rag", rag_node)

graph_builder.add_edge(START, "rag")
graph_builder.add_edge("rag", END)

graph = graph_builder.compile()


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    result = graph.invoke({
        "message": "How long does delivery take?",
        "response": "",
        "intent": "",
        "tool_result": {},
        "context": []
    })

    print("\nAgent Response:")
    print(result["response"])

    print("\nRetrieved Context:")

    for item in result["context"]:
        print(
            f"- {item['source']} "
            f"({item['method']})"
        )
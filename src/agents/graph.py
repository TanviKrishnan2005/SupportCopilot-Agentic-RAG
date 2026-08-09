from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict

from src.rag.rag_pipeline import answer_question

from src.tools.order_tools import (
    get_order_status,
    check_refund_eligibility,
    create_ticket
)


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
# Tools
# --------------------------------------------------

tools = [
    get_order_status,
    check_refund_eligibility,
    create_ticket
]

tool_node = ToolNode(tools)


# --------------------------------------------------
# Build Graph
# --------------------------------------------------

graph_builder = StateGraph(AgentState)

graph_builder.add_node("rag", rag_node)
graph_builder.add_node("tools", tool_node)

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
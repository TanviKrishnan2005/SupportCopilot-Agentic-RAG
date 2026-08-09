from langgraph.graph import StateGraph, START, END
from typing import TypedDict
import re

from src.rag.rag_pipeline import answer_question
from src.rag.rag_pipeline import llm

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
# Router
# --------------------------------------------------

def route_question(state: AgentState):

    question = state["message"].lower()

    if "order" in question and (
        "where" in question
        or "status" in question
        or "track" in question
    ):
        return {
            "intent": "order_status"
        }

    if "refund" in question:
        return {
            "intent": "refund"
        }

    if "ticket" in question or "complaint" in question:
        return {
            "intent": "ticket"
        }

    return {
        "intent": "rag"
    }


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
# Generate Final Response
# --------------------------------------------------

def generate_response(state: AgentState):

    result = state["tool_result"]
    question = state["message"]

    prompt = f"""
You are NovaCart's customer support assistant.

Answer the customer using the information provided below.

Customer question:
{question}

Support information:
{result}

Give a short, clear and helpful response.

Do not invent information.
"""

    response = llm.invoke(prompt)

    return {
        "response": response.content
    }

# --------------------------------------------------
# Tool Node
# --------------------------------------------------

def tool_node(state: AgentState):

    question = state["message"]
    intent = state["intent"]

    # Find order ID
    match = re.search(r"ORD\d+", question.upper())

    if match is None:

        result = {
            "success": False,
            "message": "Please provide a valid order ID."
        }

        return {
            "tool_result": result,
            "response": result["message"]
        }

    order_id = match.group()

    # Order status
    if intent == "order_status":

        result = get_order_status.invoke(order_id)

        return {
            "tool_result": result,
            "response": str(result)
        }

    # Refund
    if intent == "refund":

        result = check_refund_eligibility.invoke(order_id)

        return {
            "tool_result": result,
            "response": str(result)
        }

    # Create support ticket
    if intent == "ticket":

        result = create_ticket.invoke({
            "order_id": order_id,
            "issue": question
        })

        return {
            "tool_result": result,
            "response": str(result)
        }

    return {
        "tool_result": {},
        "response": "I could not determine which support tool to use."
    }


# --------------------------------------------------
# Choose Next Node
# --------------------------------------------------

def choose_next_node(state: AgentState):

    if state["intent"] == "rag":
        return "rag"

    return "tools"


# --------------------------------------------------
# Build Graph
# --------------------------------------------------

graph_builder = StateGraph(AgentState)

graph_builder.add_node("router", route_question)
graph_builder.add_node("rag", rag_node)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "router")

graph_builder.add_conditional_edges(
    "router",
    choose_next_node,
    {
        "rag": "rag",
        "tools": "tools"
    }
)

graph_builder.add_edge("rag", END)

graph_builder.add_node("response", generate_response)
graph_builder.add_edge("tools", "response")
graph_builder.add_edge("response", END)

graph = graph_builder.compile()


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    questions = [
        "How long does delivery take?",
        "Where is my order ORD1005?",
        "Can I get a refund for ORD1005?",
        "My package ORD1005 arrived damaged, create a complaint"
    ]

    for question in questions:

        result = graph.invoke({
            "message": question,
            "response": "",
            "intent": "",
            "tool_result": {},
            "context": []
        })

        print("\n" + "=" * 60)
        print("Question:", question)
        print("Intent:", result["intent"])
        print("Response:", result["response"])
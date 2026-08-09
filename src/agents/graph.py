from langgraph.graph import StateGraph, START, END
from typing import TypedDict
import re

from src.rag.rag_pipeline import answer_question, llm

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

    question = state["message"].strip().lower()

    # Empty question
    if not question:
        return {
            "intent": "fallback"
        }

    # Order status
    if "order" in question and (
        "where" in question
        or "status" in question
        or "track" in question
    ):
        return {
            "intent": "order_status"
        }

    # Refund
    if "refund" in question:
        return {
            "intent": "refund"
        }

    # Support ticket
    if "ticket" in question or "complaint" in question:
        return {
            "intent": "ticket"
        }

    # Everything else goes to RAG
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
# Fallback Node
# --------------------------------------------------

def fallback_node(state: AgentState):

    return {
        "response": "Please enter a question so I can help you."
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

    try:

        # Order status
        if intent == "order_status":

            result = get_order_status.invoke(order_id)

        # Refund
        elif intent == "refund":

            result = check_refund_eligibility.invoke(order_id)

        # Create support ticket
        elif intent == "ticket":

            result = create_ticket.invoke({
                "order_id": order_id,
                "issue": question
            })

        else:

            result = {
                "success": False,
                "message": "I could not determine which support tool to use."
            }

    except Exception:

        result = {
            "success": False,
            "message": "Something went wrong while processing your request."
        }

    return {
        "tool_result": result,
        "response": str(result)
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
# Choose Next Node
# --------------------------------------------------

def choose_next_node(state: AgentState):

    if state["intent"] == "rag":
        return "rag"

    if state["intent"] == "fallback":
        return "fallback"

    return "tools"


# --------------------------------------------------
# Build Graph
# --------------------------------------------------

graph_builder = StateGraph(AgentState)

graph_builder.add_node("router", route_question)
graph_builder.add_node("rag", rag_node)
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("response", generate_response)
graph_builder.add_node("fallback", fallback_node)

graph_builder.add_edge(START, "router")

graph_builder.add_conditional_edges(
    "router",
    choose_next_node,
    {
        "rag": "rag",
        "tools": "tools",
        "fallback": "fallback"
    }
)

graph_builder.add_edge("rag", END)

graph_builder.add_edge("tools", "response")
graph_builder.add_edge("response", END)

graph_builder.add_edge("fallback", END)

graph = graph_builder.compile()


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    question = input("\nAsk NovaCart a question: ")

    result = graph.invoke({
        "message": question,
        "response": "",
        "intent": "",
        "tool_result": {},
        "context": []
    })

    print("\n" + "=" * 60)
    print("NOVACART SUPPORT")
    print("=" * 60)

    print("\nIntent:", result["intent"])
    print("\nResponse:", result["response"])
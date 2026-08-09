from langgraph.graph import StateGraph, START, END
from typing import TypedDict


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
# Agent Node
# --------------------------------------------------

def agent_node(state: AgentState):

    message = state["message"]

    return {
        "response": f"Agent received: {message}"
    }


# --------------------------------------------------
# Build Graph
# --------------------------------------------------

graph_builder = StateGraph(AgentState)

graph_builder.add_node("agent", agent_node)

graph_builder.add_edge(START, "agent")
graph_builder.add_edge("agent", END)

graph = graph_builder.compile()


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    result = graph.invoke({
        "message": "Where is my order ORD1005?",
        "response": "",
        "intent": "",
        "tool_result": {},
        "context": []
    })

    print("\nAgent State:")
    print(result)
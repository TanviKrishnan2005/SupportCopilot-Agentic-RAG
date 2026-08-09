from langgraph.graph import StateGraph, START, END
from typing import TypedDict


class AgentState(TypedDict):
    message: str
    response: str


def agent_node(state: AgentState):

    message = state["message"]

    return {
        "response": f"Agent received: {message}"
    }


graph_builder = StateGraph(AgentState)

graph_builder.add_node("agent", agent_node)

graph_builder.add_edge(START, "agent")
graph_builder.add_edge("agent", END)

graph = graph_builder.compile()


if __name__ == "__main__":

    result = graph.invoke({
        "message": "Hello NovaCart!",
        "response": ""
    })

    print(result["response"])
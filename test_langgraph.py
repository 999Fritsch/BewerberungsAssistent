from typing import Annotated, Literal
import multiprocessing
import json

from typing_extensions import TypedDict

from langchain_core.messages import ToolMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_community.chat_models import ChatLlamaCpp
from langchain_community.tools import DuckDuckGoSearchResults

class State(TypedDict):
    messages: Annotated[list, add_messages]

class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""

    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: dict) -> dict:
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No messages in inputs.")
        outputs = []
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"]
                )
            )
        return {"messages": outputs}
        

graph_builder = StateGraph(State)

tool = DuckDuckGoSearchResults(output_format="json", num_results=2)
tools = [tool]
tool_node = BasicToolNode(tools=tools)

# Path to your model weights
local_model = "Phi-3.5-mini-instruct-IQ4_XS.gguf"

llm = ChatLlamaCpp(
    temperature=0.5,
    model_path=local_model,
    n_ctx=10000,
    n_gpu_layers=0,
    n_batch=300,  # Adjust based on your system resources
    max_tokens=512,
    n_threads=multiprocessing.cpu_count() - 2,
    repeat_penalty=1.5,
    top_p=0.5,
    verbose=False,
)
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

def route_tools(state: State):
    """Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end."""

    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END

# The `tools_condition` function returns "tools" if the chatbot asks to use a tool, and "END" if
# it is fine directly responding. This conditional routing defines the main agent loop.
graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    # The following dictionary lets you tell the graph to interpret the condition's outputs as a specific node
    # It defaults to the identity function, but if you
    # want to use a node named something else apart from "tools",
    # You can update the value of the dictionary to something else
    # e.g., "tools": "my_tools"
    {"tools": "tools", END: END},
)
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")

graph_builder.add_node("tools", tool_node)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")

graph = graph_builder.compile()

graph_image = graph.get_graph().draw_mermaid_png()
with open("/home/fritsch/Documents/projects/BewerberungsAssistent/graph_image.png", "wb") as f:
    f.write(graph_image)

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User:", user_input)
        stream_graph_updates(user_input)
        break



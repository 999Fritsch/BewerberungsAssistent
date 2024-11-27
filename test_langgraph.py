from typing import Annotated
import multiprocessing
import json

from typing_extensions import TypedDict

from langchain_core.messages import ToolMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_community.chat_models import ChatLlamaCpp
from langchain_community.tools import DuckDuckGoSearchResults

# Define the state structure
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Define the chatbot function
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Function to stream graph updates based on user input
def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [("user", user_input)]}, config):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

# Initialize the state graph
graph_builder = StateGraph(State)

# Initialize memory saver
memory = MemorySaver()

# Initialize the configuration
config = {"configurable": {"thread_id": "1"}}

# Initialize tools
tool = DuckDuckGoSearchResults(output_format="json", num_results=2)
tools = [tool]
tool_node = ToolNode(tools=[tool])

# Path to your model weights
local_model = "Phi-3.5-mini-instruct-IQ4_XS.gguf"

# Initialize the language model
llm = ChatLlamaCpp(
    temperature=0.5,
    model_path=local_model,
    n_ctx=10000,
    n_gpu_layers=0,
    n_batch=2048,  # Adjust based on your system resources
    max_tokens=512,
    n_threads=multiprocessing.cpu_count() - 2,
    repeat_penalty=1.5,
    top_p=0.5,
    verbose=False,
)
llm_with_tools = llm.bind_tools(tools)

# Add conditional edges to the graph
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

# Add edges to the graph
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

# Add nodes to the graph
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("chatbot", chatbot)

# Compile the graph
graph = graph_builder.compile(checkpointer=memory)

# Generate and save the graph image
graph_image = graph.get_graph().draw_mermaid_png()
with open("/home/fritsch/Documents/projects/BewerberungsAssistent/graph_image.png", "wb") as f:
    f.write(graph_image)

# Main loop to interact with the user
while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except:
        # Fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User:", user_input)
        stream_graph_updates(user_input)
        break



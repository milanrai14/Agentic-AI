from langgraph.graph import StateGraph, START
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_community.tools import DuckDuckGoSearchRun
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
import sys
from pathlib import Path

load_dotenv()  # Load environment variables from .env file

llm = ChatOllama(model='llama3.2')

#MCP client for the local FastMCP server

    # Locate the MCP server file
server_path = (
    Path(__file__).parent
        / "mcp_server"
        / "arithmetic_server.py"
    )

    # Configure MCP server connection
client = MultiServerMCPClient(
        {
            "arithmetic": {
                "transport": "stdio",
                "command": sys.executable,
                "args": [str(server_path)]
            }
        }
    )



# state
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


async def build_graph():
    tools = await client.get_tools()
    print(tools)

    llm_with_tools = llm.bind_tools(tools)

    # nodes
    async def chat_node(state: ChatState): 
        messages = state['messages']
        response = await llm_with_tools.ainvoke(messages)
        return {'messages': [response]}
    
    tool_node = ToolNode(tools)

    #definig graph and nodes 
    graph = StateGraph(ChatState)

    graph.add_node("chat_node", chat_node)
    graph.add_node("tools", tool_node)

    #defining graph connection
    graph.add_edge(START, "chat_node")
    graph.add_conditional_edges("chat_node", tools_condition)
    graph.add_edge("tools", "chat_node")


    chatbot = graph.compile()

    return chatbot 

async def main(): 
    chatbot =await build_graph()
    result =  await chatbot.ainvoke({"messages": [HumanMessage(content="Find the modulus of 132354 and 23 and give answer like a cricket commentator.")]})
    print(result['messages'][-1].content)

if __name__ == '__main__': 
    asyncio.run(main())
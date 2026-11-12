from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_ollama import ChatOllama
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

import requests
import random
import os
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver


load_dotenv()
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

def get_llm(): 
    llm = ChatOllama(model='llama3.2')
    return llm

#tools 
search_tool = DuckDuckGoSearchRun(region='us-en')

@tool
def calculator(first_num: float, second_num: float, operation: str)->dict: 
    """
    Perform a basic arithematic operation on two numbers.
    Supported operation: add, sub, mul, div 
    """
    try: 
        if operation == 'add': 
            result = first_num + second_num
        elif operation == 'sub': 
            result = first_num - second_num
        elif operation == 'mul': 
            result = first_num * second_num
        elif operation == 'div': 
            if second_num == 0: 
                return {"error": "Division by zero is not allowed"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation {operation}"}
        return{ "first_num": first_num, "Second_num": second_num, "Operation": operation, "result": result}
    except Exception as e:
        return {"error": str(e)}

@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch the latest stock price for a given symbol
    (e.g. AAPL, TSLA) using Alpha Vantage API.
    """

    url = "https://www.alphavantage.co/query"

    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol.upper(),
        "apikey": API_KEY
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    quote = data.get("Global Quote")

    if not quote:
        return {
            "error": data.get("Note")
                     or data.get("Error Message")
                     or "Stock data unavailable."
        }

    return {
        "symbol": quote.get("01. symbol"),
        "price": quote.get("05. price"),
        "change": quote.get("09. change"),
        "change_percent": quote.get("10. change percent")
    }

# Make tool list 
tools = [get_stock_price, search_tool, calculator]

# make  the llm tool awate
llm = get_llm()

llm_with_tools = llm.bind_tools(tools)

#State
class ChatState(TypedDict): 
    messages: Annotated[list[BaseMessage], add_messages]

#Graph nodes 
def chat_node(state: ChatState):
    """LLM node that may answer or request a tool call."""
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    return {'messages': [response]}

tool_node = ToolNode(tools) # Executes tool calls


conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)
#graph structure
graph = StateGraph(ChatState)
graph.add_node('chat_node', chat_node)
graph.add_node('tools', tool_node)

#Edges 
graph.add_edge(START, "chat_node")

# If the LLM asked for a tool, go to ToolNode; elsse finish
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")

chatbot = graph.compile(checkpointer=checkpointer)

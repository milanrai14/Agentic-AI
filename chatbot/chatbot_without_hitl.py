from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from dotenv import load_dotenv
import requests

load_dotenv()

#LLM
llm = ChatOllama(model="llama3.2")

#tools 
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

@tool
def purchase_stock(symbol: str, quantity: int) -> dict: 
    """
    Simulate purchasing a given quantity of a stock symbol.
    Note: this is a mock implementaiton: 
    - No real brokerage API is called.
    - It simply returns a confirmation payload.
    """
    return{
        "status": "success", 
        "message": f"Purchase order placed for {quantity} shares of  {symbol}", 
        "symbol": symbol, 
        "quantity": quantity
    }

tools = [get_stock_price, purchase_stock]

llm_with_tools = llm.bind_tools(tools)

#State 
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# nodes
def chat_node(state: ChatState): 
    """
    LLM node that may answer or request a tool call.
    """
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools)

#checkpointer 
memory =  MemorySaver()

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")

graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")

chatbot = graph.compile(checkpointer=memory)

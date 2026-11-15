from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import interrupt, Command
from langchain_core.tools import tool
from dotenv import load_dotenv
import requests
import os

load_dotenv()
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
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

    #this pauses the graph and returns control to the caller 
    decision = interrupt(f"Approve buying {quantity} shares of {symbol}? (yes/no)")
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
# 7. Simple usage example (CLI)
# -------------------
if __name__ == "__main__":
    print("📈 Stock Bot with Tools (get_stock_price, purchase_stock)")
    print("Type 'exit' to quit.\n")

    # thread_id still works with MemorySaver (conversation kept in RAM)
    thread_id = "demo-thread"

    while True:
        user_input = input("You: ")
        if user_input.lower().strip() in {"exit", "quit"}:
            print("Goodbye!")
            break

        # Build initial state for this turn
        state = {"messages": [HumanMessage(content=user_input)]}

        # Run the graph
        result = chatbot.invoke(
            state,
            config={"configurable": {"thread_id": thread_id}},
        )

        # Get the latest message from the assistant
        messages = result["messages"]
        last_msg = messages[-1]
        print(f"Bot: {last_msg.content}\n")
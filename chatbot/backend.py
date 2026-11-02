from langgraph.graph import StateGraph, START, END
from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver

from langgraph.graph.message import add_messages
class ChatState(TypedDict): 
    messages: Annotated[list[BaseMessage], add_messages]
    
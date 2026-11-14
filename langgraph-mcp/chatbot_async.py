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
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.tools import tool
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from langgraph.graph import  StateGraph, START, END
from typing import Annotated, TypedDict, Dict, Any, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.prebuilt import ToolNode, tools_condition
import os

load_dotenv()
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

def get_llm(): 
    llm = ChatOllama(model='llama3.2')
    return llm

# -------------------
# 2. PDF retriever store (per thread)
# -------------------
_THREAD_RETRIEVERS: Dict[str, Any] = {}
_THREAD_METADATA: Dict[str, dict] = {}

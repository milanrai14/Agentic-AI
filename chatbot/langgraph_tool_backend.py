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

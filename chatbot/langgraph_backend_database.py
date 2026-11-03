import sqlite3

from langgraph.graph import StateGraph, START, END
from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_ollama import ChatOllama
from langgraph.checkpoint.sqlite import SqliteSaver 

from langgraph.graph.message import add_messages
class ChatState(TypedDict): 
    messages: Annotated[list[BaseMessage], add_messages]

llm = ChatOllama(model='llama3.2')

sqlite3.connector(database='chatbot.db', check_same_thread=False)
def chat_node(state: ChatState): 
    #take a user query from state
    messages = state['messages']

    # send to llm
    response = llm.invoke(messages) 

    # response store state
    return {"messages": response}

checkpointer = SqliteSaver()
graph = StateGraph(ChatState)

#add nodes
graph.add_node("chat_node", chat_node)

#add edges 
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)
chatbot = graph.compile(checkpointer=checkpointer)



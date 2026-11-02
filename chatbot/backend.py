from langgraph.graph import StateGraph, START, END
from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver

from langgraph.graph.message import add_messages
class ChatState(TypedDict): 
    messages: Annotated[list[BaseMessage], add_messages]

llm = ChatOllama(model='llama3.2')

def chat_node(state: ChatState): 
    #take a user query from state
    messages = state['messages']

    # send to llm
    response = llm.invoke(messages) 

    # response store state
    return {"messages": response}

checkpointer = MemorySaver()
graph = StateGraph(ChatState)

#add nodes
graph.add_node("chat_node", chat_node)

#add edges 
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)
chatbot = graph.compile(checkpointer=checkpointer)


# inital_state = {
#     "messages": [HumanMessage(content="What is the capital of Nepal?")]
# }
# chatbot.invoke(inital_state)['messages'][-1].content

# thread_id = '1'
# while True:
#     user_message = input("type : ")
#     print("User: ", user_message)

#     if user_message.strip().lower() in ['exit', 'quit', 'bye', '0']:
#         break
#     config = {'configurable': {'thread_id': thread_id}}
#     response = chatbot.invoke({

#         'messages': [HumanMessage(content=user_message)]
#     }, config=config)

#     print('AI: ', response['messages'][-1].content)
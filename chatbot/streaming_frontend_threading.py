import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage
import uuid

#Utility function
def generate_thread_id(): 
    thread_id = uuid.uuid4()
    return thread_id

#st.session_state -> dict -> 

if 'message_history' not in st.session_state: 
    st.session_state['message_history'] = []

    if 'thread_id' not in st.session_state: 
        st.session_state['thread_id'] = generate_thread_id()
        

#Sidebar UI 
st.sidebar.title("LangGraph Chatbots")
st.sidebar.button("New Chat")
st.sidebar.header("My conversation")
#loadin the conversation history
for message in st.session_state['message_history']: 
    with st.chat_message(message['role']): 
        st.text(message['content'])
# {'role': 'user', 'content': 'Hi'}

user_input = st.chat_input("Type here ")



if user_input:
    # First, add the user message to message history
    st.session_state['message_history'].append({
        'role': 'user',
        'content': user_input
    })

    with st.chat_message("user"):
        st.text(user_input)

    # Stream the response from LangGraph
    response = chatbot.stream(
        {"messages": [HumanMessage(content=user_input)]},
        config={"configurable": {"thread_id": "milan_12"}},
        stream_mode="messages"
    )

    ai_messages = ""

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        for message_chunk, metadata in response:
            if message_chunk.content:
                ai_messages += message_chunk.content
                message_placeholder.markdown(ai_messages)

    # Save the completed AI response to Streamlit history
    st.session_state['message_history'].append({
        'role': 'assistant',
        'content': ai_messages
    })

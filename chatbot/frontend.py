import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage
#st.session_state -> dict -> 

if 'message_history' not in st.session_state: 
    st.session_state['message_history'] = []
# message_history = []

#loadin the conversation history
for message in st.session_state['message_history']: 
    with st.chat_message(message['role']): 
        st.text(message['content'])
# {'role': 'user', 'content': 'Hi'}

user_input = st.chat_input("Type here ")


if user_input: 
    #first add the message to message history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message("user"):
        st.text(user_input)
    response = chatbot.invoke({"messages": [HumanMessage(content=user_input)]})
    ai_messages= response['messages'][-1].content
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_messages})
    with st.chat_message("assistant"): 
        st.text(ai_messages)
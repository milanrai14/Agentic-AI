import streamlit as st

message_history = []

#loadin the conversation history
for message in message_history: 
    with st.chat_message(message['role']): 
        st.text(message['content'])
# {'role': 'user', 'content': 'Hi'}

user_input = st.chat_input("Type here ")


if user_input: 
    #first add the message to message history
    message_history.append({'role': 'user', 'content': user_input})
    with st.chat_message("user"):
        st.text(user_input)

    message_history.append({'role': 'assistant', 'content': user_input})
    with st.chat_message("assistant"): 
        st.text(user_input)
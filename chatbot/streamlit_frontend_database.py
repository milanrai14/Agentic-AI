
import streamlit as st
from dotenv import load_dotenv
from langgraph_backend_database import chatbot, retrive_all_threads
from langchain_core.messages import HumanMessage
import uuid


load_dotenv()
# Utility function
def generate_thread_id():
    return str(uuid.uuid4())

def add_thread(thread_id): 
    if thread_id not in st.session_state['chat_threads']: 
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    state = chatbot.get_state(config)

    # Check whether the thread has a saved state
    if not state or not state.values:
        return []

    # Safely retrieve messages
    return state.values.get("messages", [])
# Reset chat
def reset_chat():
    st.session_state["thread_id"] = generate_thread_id()
    add_thread(st.session_state['thread_id'])
    st.session_state["message_history"] = []


# Initialize session state independently
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if 'chat_threads' not in st.session_state: 
    st.session_state['chat_threads'] = retrive_all_threads()
    
add_thread(st.session_state['thread_id'])
    
# Sidebar UI
st.sidebar.title("LangGraph Chatbots")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My conversation")
# st.sidebar.caption(
#     f"Thread ID: {st.session_state['thread_id']}"
# )

for thread_id in st.session_state['chat_threads']: 
    if st.sidebar.button( f"Thread ID: {thread_id}"): 
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_message_dict =  []

        for message in messages: 
            if isinstance(messages, HumanMessage): 
                role='user'
            else: 
                role='assistant'
            temp_message_dict.append({'role': role, 'content': message.content})
        st.session_state['message_history'] = temp_message_dict



# Load conversation history
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User input
user_input = st.chat_input("Type here")

if user_input:
    # Save and display user message
    st.session_state["message_history"].append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Stream LangGraph response
    response = chatbot.stream(
        {"messages": [HumanMessage(content=user_input)]},
        config={
            "configurable": {
                "thread_id": st.session_state["thread_id"]
            }
        },
        stream_mode="messages"
    )

    ai_messages = ""

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        for message_chunk, metadata in response:
            if message_chunk.content:
                ai_messages += str(message_chunk.content)
                message_placeholder.markdown(ai_messages)

    # Save AI response
    st.session_state["message_history"].append({
        "role": "assistant",
        "content": ai_messages
    })

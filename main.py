import streamlit as st
import requests
import uuid

height = 500
width = 700

st.title("CAT VARC CHATBOT", width = 700)
passage = st.text_area("Enter passage here", height=height, width=width)
st.sidebar.button("New Chat")

# generating thread id

def generate_thread_id():
    return str(uuid.uuid4())

if "thread_id" not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# loading the conversation history

for message in st.session_state['message_history']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input at bottom
user_input = st.chat_input("Type here")

if user_input:
    # first add the message to message_history
    st.session_state['message_history'].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    payload = {
        "passage":passage,
        "user_query": user_input,
        "thread_id": st.session_state["thread_id"]
    }
    response = requests.post("http://localhost:8000/ask", json=payload)
    print(response.json())
    ai_message = response.json()["final_answer"]

    with st.chat_message("assistant"):
        ai_message = st.write(ai_message)
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
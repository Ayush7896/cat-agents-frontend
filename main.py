import streamlit as st
import uuid
import streamlit as st
import requests
import uuid

height = 500
width = 700

st.title("CAT VARC CHATBOT", width=700)
passage = st.text_area("Enter passage here", height=height, width=width)

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
# CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

if user_input:
    # add user message to history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # Create payload
    payload = {
        "passage": passage,
        "user_query": user_input,
        "thread_id": st.session_state["thread_id"]
    }
    

    # ✅ Pass passage + user_query + conversation_messages
    response =requests.post("http://localhost:8000/ask", json=payload)
    
    # print(response)
    print(response)
    print(type(response))
    print(response.json())


    response_data = response.json()
    ai_message = response_data['final_answer']   # synthesizer agent gives this
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)




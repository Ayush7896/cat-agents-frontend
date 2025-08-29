import streamlit as st
import requests
import uuid

# Assign thread_id (conversation_id) once per new chat
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(uuid.uuid4())   # persistent per chat

st.title("CAT VARC Chatbot")
height = 500
width = 700

# st.title("Smarter Prep for CAT VARC", width = 700)
# st.text_area(label = "Put passage here", height=height, width=width)
passage = st.text_area("Enter passage",height=height, width=width)
user_input = st.chat_input("Ask me anything")

if user_input:
    payload = {
        "passage": passage,
        "user_query": user_input,
        "thread_id": st.session_state["thread_id"]   # persistent!
    }
    response = requests.post("http://localhost:8000/ask", json=payload)
    print(response)
    print(response.json())
    ai_message = response.json()["final_answer"]

    # Save locally for UI rendering
    if "history" not in st.session_state:
        st.session_state["history"] = []
    st.session_state["history"].append(("user", user_input))
    st.session_state["history"].append(("assistant", ai_message))

# Display history
for role, msg in st.session_state.get("history", []):
    with st.chat_message(role):
        st.markdown(msg)

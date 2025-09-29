import streamlit as st
import sys
import os
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.auth_utils import is_authenticated, get_headers
import uuid 

# check if logged in
if not is_authenticated():
    st.error("Please login to access chatbot")
    st.stop()

# simple chat interface
height = 500
width = 700
API_URL = os.environ.get("API_URL", "http://localhost:8000")

st.title("CAT VARC CHATBOT")
passage = st.text_area("Enter passage here", height=height, width=width)

# generating thread id
def generate_thread_id():
    return str(uuid.uuid4())

if "thread_id" not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Store last Q&A for corrections
if 'last_qa' not in st.session_state:
    st.session_state['last_qa'] = {}

# loading the conversation history
for i, message in enumerate(st.session_state['message_history']):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Show feedback buttons only if last message is from assistant
if st.session_state['message_history']:
    last_message = st.session_state['message_history'][-1]
    
    if last_message["role"] == "assistant":
        # FEEDBACK BUTTONS
        st.markdown("---")
        st.markdown("### 🎯 Was this answer correct?")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ YES, CORRECT", key="btn_correct", use_container_width=True, type="primary"):
                st.success("Thanks for the feedback!")
                st.balloons()
        
        with col2:
            if st.button("❌ NO, WRONG", key="btn_wrong", use_container_width=True, type="secondary"):
                st.session_state['show_correction'] = True
                st.rerun()

# Show correction form when user clicks "Wrong"
if st.session_state.get('show_correction', False):
    st.markdown("---")
    st.markdown("### 📝 Help us improve!")
    
    with st.container():
        st.write("**Question:**", st.session_state.last_qa.get('question', 'No question stored'))
        st.write("**My answer:**", st.session_state.last_qa.get('answer', 'No answer stored'))
        
        correct_answer = st.text_area("What's the correct answer?", key="correction_text", height=100)
        explanation = st.text_area("Why is this the correct answer? (optional):", key="explanation_text", height=80)
        
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            if st.button("💾 Submit Correction", use_container_width=True, type="primary"):
                if correct_answer.strip():
                    # Save correction
                    headers = get_headers()
                    try:
                        response = requests.post(
                            f"{API_URL}/feedback/correct-answer",
                            json={
                                "passage": st.session_state.last_qa.get('passage', ''),
                                "question": st.session_state.last_qa.get('question', ''),
                                "wrong_answer": st.session_state.last_qa.get('answer', ''),
                                "correct_answer": correct_answer,
                                "explanation": explanation
                            },
                            headers=headers
                        )
                        
                        if response.status_code == 200:
                            st.success("✅ Correction saved! I'll remember this.")
                            st.session_state['show_correction'] = False
                            st.rerun()
                        else:
                            st.error(f"❌ Failed to save: {response.status_code}")
                    except Exception as e:
                        st.error(f"❌ Error saving correction: {e}")
                else:
                    st.warning("Please enter the correct answer before submitting.")
        
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state['show_correction'] = False
                st.rerun()

# Chat input at bottom
user_input = st.chat_input("Ask a question about the passage...")

if user_input:
    # add user message to history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    
    # Create payload
    payload = {
        "passage": passage,
        "user_query": user_input,
        "thread_id": st.session_state["thread_id"]
    }
    
    # Store Q&A for potential correction
    st.session_state['last_qa'] = {
        'passage': passage,
        'question': user_input,
        'answer': ''  # Will be filled with response
    }
    
    headers = get_headers()
    try:
        # Make API request
        with st.spinner("Thinking..."):
            response = requests.post(f"{API_URL}/ask", json=payload, headers=headers)
        
        if response.status_code == 200:
            response_data = response.json()
            
            if 'final_answer' in response_data:
                ai_message = response_data['final_answer']
                
                # Store the answer for correction
                st.session_state['last_qa']['answer'] = ai_message
                
                # Check if this is a corrected answer
                if "*Note: This answer is based on previous user feedback*" in ai_message:
                    ai_message = f"✅ {ai_message}"
                
                st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
                # Display the message immediately
                with st.chat_message('assistant'):
                    st.markdown(ai_message)
                # Force rerun to show buttons
                st.rerun()
            else:
                st.error(f"Unexpected response format: {response_data}")
        else:
            try:
                error_detail = response.json().get('detail', 'Unknown error')
                st.error(f"Server error ({response.status_code}): {error_detail}")
            except:
                st.error(f"Server error ({response.status_code}): {response.text}")
                
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")








# import streamlit as st
# import sys
# import os
# import requests
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from utils.auth_utils import is_authenticated, get_headers
# import uuid 


# # check if logged in
# if not is_authenticated():
#     st.error("Please login to access chatbot")
#     st.stop()

# # simple chat interface
# height = 500
# width = 700
# API_URL = os.environ.get("API_URL", "http://localhost:8000")

# st.title("CAT VARC CHATBOT", width=700)
# passage = st.text_area("Enter passage here", height=height, width=width)

# # generating thread id
# def generate_thread_id():
#     return str(uuid.uuid4())

# if "thread_id" not in st.session_state:
#     st.session_state['thread_id'] = generate_thread_id()

# if 'message_history' not in st.session_state:
#     st.session_state['message_history'] = []

# # loading the conversation history
# for message in st.session_state['message_history']:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Chat input at bottom
# user_input = st.chat_input("Type here")

# if user_input:
#     # add user message to history
#     st.session_state['message_history'].append({'role': 'user', 'content': user_input})
#     with st.chat_message('user'):
#         st.text(user_input)

#     # Create payload
#     payload = {
#         "passage": passage,
#         "user_query": user_input,
#         "thread_id": st.session_state["thread_id"]
#     }
#     headers = get_headers()
#     try:
#         # Make API request
#         response = requests.post(f"{API_URL}/ask", json=payload, headers=headers)
        
#         print(f"Status Code: {response.status_code}")
#         print(f"Raw response: {response.text}")
        
#         if response.status_code == 200:
#             response_data = response.json()
            
#             # Check if final_answer exists in response
#             if 'final_answer' in response_data:
#                 ai_message = response_data['final_answer']
#                 st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
#                 with st.chat_message('assistant'):
#                     st.markdown(ai_message)  # Use markdown instead of text for better formatting
#             else:
#                 st.error(f"Unexpected response format: {response_data}")
#                 print(f"Available keys: {response_data.keys() if isinstance(response_data, dict) else 'Not a dict'}")
#         else:
#             # Handle HTTP errors
#             try:
#                 error_detail = response.json().get('detail', 'Unknown error')
#                 st.error(f"Server error ({response.status_code}): {error_detail}")
#             except:
#                 st.error(f"Server error ({response.status_code}): {response.text}")
                
#     except requests.exceptions.RequestException as e:
#         st.error(f"Connection error: {e}")
#     except Exception as e:
#         st.error(f"Unexpected error: {e}")

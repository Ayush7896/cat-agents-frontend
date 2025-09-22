# import streamlit as st
# import uuid
# import streamlit as st
# import requests
# import uuid
# import os

# height = 500
# width = 700
# API_URL = os.environ.get("API_URL", "https://cat-agents-backend-production.up.railway.app")

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
# # CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

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
    

#     # ✅ Pass passage + user_query + conversation_messages
#     response = requests.post(f"{API_URL}/ask", json=payload)
    
#     # print(response)
#     print(response)
#     print(type(response))
#     print(response.json())


#     response_data = response.json()
#     ai_message = response_data['final_answer']   # synthesizer agent gives this
#     st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
#     with st.chat_message('assistant'):
#         st.text(ai_message)



# import streamlit as st
# import uuid
# import streamlit as st
# import requests
# import uuid
# import os

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
# # CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

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
    

#     # ✅ Pass passage + user_query + conversation_messages
#     response = requests.post(f"{API_URL}/ask", json=payload)
    
#     # print(response)
#     print(response)
#     print(type(response))
#     print(response.json())
#     print(f"Raw response: {response.text}")



#     response_data = response.json()
#     ai_message = response_data['final_answer']   # synthesizer agent gives this
#     st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
#     with st.chat_message('assistant'):
#         st.text(ai_message)



import streamlit as st
import uuid
import requests
import os

height = 500
width = 700
API_URL = os.environ.get("API_URL", "http://localhost:8000")

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
    
    try:
        # Make API request
        response = requests.post(f"{API_URL}/ask", json=payload)
        
        print(f"Status Code: {response.status_code}")
        print(f"Raw response: {response.text}")
        
        if response.status_code == 200:
            response_data = response.json()
            
            # Check if final_answer exists in response
            if 'final_answer' in response_data:
                ai_message = response_data['final_answer']
                st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
                with st.chat_message('assistant'):
                    st.markdown(ai_message)  # Use markdown instead of text for better formatting
            else:
                st.error(f"Unexpected response format: {response_data}")
                print(f"Available keys: {response_data.keys() if isinstance(response_data, dict) else 'Not a dict'}")
        else:
            # Handle HTTP errors
            try:
                error_detail = response.json().get('detail', 'Unknown error')
                st.error(f"Server error ({response.status_code}): {error_detail}")
            except:
                st.error(f"Server error ({response.status_code}): {response.text}")
                
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
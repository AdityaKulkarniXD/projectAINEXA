from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro Model and get response
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize Streamlit
page_title = "AINEXA"
page_icon = "favicon.png"
st.set_page_config(page_title=page_title, page_icon=page_icon)
st.header("Career Guidance")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'input' not in st.session_state:
    st.session_state['input'] = ""
if 'clear_input' not in st.session_state:
    st.session_state['clear_input'] = False

def process_input():
    input = st.session_state.input
    if input:
        response = get_gemini_response(input)
        # Add user query to session chat history
        st.session_state['chat_history'].append(("You", input))
        st.subheader("The response is")
        for chunk in response:
            modified_text = chunk.text.replace("Gemini", "AINEXA")
            modified_text = modified_text.replace("Google", "Aditya Kulkarni")
            st.write(modified_text)
            st.session_state['chat_history'].append(("Bot", modified_text))
        st.session_state.clear_input = True  # Set the flag to clear input

# Check if we need to clear the input
if st.session_state.clear_input:
    st.session_state.input = ""
    st.session_state.clear_input = False

st.text_area("Input: ", key="input", on_change=process_input)

if st.button("Ask the Question"):
    process_input()

st.subheader("The Chat history is")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")

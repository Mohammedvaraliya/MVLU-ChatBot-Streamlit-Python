import streamlit as st
import time
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv() 
api_key = os.getenv("GOOGLE_GEMINI_API_KEY")

genai.configure(api_key=api_key)

if "generation_config" not in  st.session_state:
    st.session_state["generation_config"] = {
    "temperature": 0.5,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
    }

if "safety_setting" not in  st.session_state:
    st.session_state["safety_settings"] = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

if "model" not in st.session_state:
    st.session_state["model"] = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=st.session_state["generation_config"],
                              safety_settings=st.session_state["safety_settings"])

if "convo" not in st.session_state and "model" in st.session_state:
    with open("./assets/dataset_2.json") as file:
        st.session_state["convo"] = st.session_state["model"].start_chat(history=json.load(file))

st.title("MVLU College Chatbot")

def stream_data(text:str):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05)


for message in st.session_state["convo"].history[18:]:
    with st.chat_message("Gemini" if message.role == "model" else "User"):
        st.markdown(message.parts[0].text)


if prompt := st.chat_input("What is up?"):
    with st.chat_message("User"):
        st.markdown(prompt)
        
    response = st.session_state["convo"].send_message(prompt)
    
 
        
    print(st.session_state["convo"].history)
    print(st.session_state["model"].count_tokens(st.session_state["convo"].history))

    with st.chat_message("Gemini"):
        stream = stream_data(response.text)
        response = st.write_stream(stream)

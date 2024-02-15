import streamlit as st
import time
import google.generativeai as genai
import json

genai.configure(api_key="AIzaSyAd67rIjm4g5SERQ--pryKK1SCCXnE3JwE")

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
    with open("./assets/dataset.json") as file:
        st.session_state["convo"] = st.session_state["model"].start_chat(history=json.load(file))

st.title("MVLU College Chatbot")

def stream_data(text:str):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.25)


for message in st.session_state["convo"].history[6:]:
    with st.chat_message("Gemini" if message.role == "model" else "User"):
        st.markdown(message.parts[0].text)


if prompt := st.chat_input("What is up?"):
    with st.chat_message("User"):
        st.markdown(prompt)
        
    response = st.session_state["convo"].send_message(prompt)
    
 
        
    print(st.session_state["convo"].history)

    with st.chat_message("Gemini"):
        stream = stream_data(response.text)
        response = st.write_stream(stream)

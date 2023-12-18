
import os
import streamlit as st
from langchain.llms import OpenAI

os.environ["OPENAI_API_KEY"] = "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"

llm = OpenAI(temperature=.9)

st.title("chatgpt")
open_ai_key = st.sidebar.text_input("key", type='password')

def generate(text):
    st.info(llm(text))
    
with st.form('my_form'):
    text = st.text_area('enter text', 'what is machine learning')
    submitted= st.form_submit_button('submit')
    if not open_ai_key.startswith('sk'):
        st.warning("not good key")
    if submitted:
        generate(text)
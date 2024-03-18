# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15

@author: Oyasi
"""



import logging
import sys
import time
from typing import Optional
import requests
import streamlit as st
from dotenv import load_dotenv
import os

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format, stream=sys.stdout, level=logging.INFO)

BASE_API_URL = "http://localhost:7860/api/v1/process"
FLOW_ID = "fa78d8a1-3da5-4c2d-bf49-fcb84a864931"

TWEAKS = {
    "PromptTemplate-whWRD": {},
    "PyPDFLoader-uYaI5": {"file_path": "<filepath>"}, ## adding the param that we want to manipulate 
    "LLMChain-HMbhy": {},
    "BaseLLM-JIibp": {}
}

BASE_AVATAR_URL = "https://raw.githubusercontent.com/garystafford-aws/static-assets/main/static"

load_dotenv()

def run_flow(inputs: dict, flow_id: str, tweaks: Optional[dict] = None) -> dict:
    api_url = f"{BASE_API_URL}/{flow_id}"
    payload = {"inputs": inputs}
    if tweaks:
        payload["tweaks"] = tweaks
    response = requests.post(api_url, json=payload)
    return response.json()

def generate_response(prompt, filepath):
    logging.info(f"input: {prompt}, file_path={filepath}")
    inputs = {"question": prompt, "file_path": filepath}

    response = run_flow(inputs, flow_id=FLOW_ID, tweaks=TWEAKS)
    
    try:
        result = response.get('result', {})
        if 'text' in result:
            logging.info(f"answer: {result['text']}")
            return result['text']
        elif 'response' in result:
            logging.info(f"answer: {result['response']}")
            return result['response']
        else:
            logging.error(f"Unexpected response format: {response}")
            return "Sorry, there was a problem finding an answer for you."
    except Exception as exc:
        logging.error(f"error: {response}")
        return "Sorry, there was a problem finding an answer for you."

def main(): 
    st.set_page_config(page_title="MSF Bot")
    st.markdown("##### Welcome to the MSF Virtual Bot")

    # Upload a PDF file
    pdf_file = st.file_uploader("Upload your PDF", type='pdf')

    filepath = None

    if pdf_file:
        filepath = pdf_file.name
        st.info("PDF uploaded successfully!")
        TWEAKS["PyPDFLoader-uYaI5"]["file_path"] = os.path.abspath(filepath)
        # Now, TWEAKS dictionary is updated with the actual file path
        # You can proceed with further logic
    else:
        st.warning("Please upload a PDF file.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.write(message["content"])

    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
                "avatar": f"{BASE_AVATAR_URL}/people-64px.png",
            }
        )
        with st.chat_message(
            "user",
            avatar=f"{BASE_AVATAR_URL}/people-64px.png",
        ):
            st.write(prompt)

        with st.chat_message(
            "assistant",
            avatar=f"{BASE_AVATAR_URL}/bartender-64px.png",
        ):
            message_placeholder = st.empty()
            with st.spinner(text="Thinking..."):
                assistant_response = generate_response(prompt, filepath)
                message_placeholder.write(assistant_response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_response,
                "avatar": f"{BASE_AVATAR_URL}/bartender-64px.png",
            }
        )

if __name__ == "__main__":
    main()

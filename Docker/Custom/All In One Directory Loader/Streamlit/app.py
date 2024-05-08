# -*- coding: utf-8 -*-
"""
Created on 6 May 2024

@author: oyasi
"""

#%%
# Pre-requisite 

# pip install streamlit
# pip3 install streamlit-extras

# To run the app use: streamlit run xxx.py
# To run the app while setting the base to dark use: streamli run xxx.py --theme.base='dark' 



#%%
# Imports 


from typing import Optional


import logging
import sys
import requests
import streamlit as st
import os




log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format, stream=sys.stdout, level=logging.INFO)

BASE_API_URL = "http://localhost:7860/api/v1/process"
FLOW_ID = "f4226ea1-9e50-4063-8fc4-86acb6dde48e"
# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
  "Data-EmHbu": {},
  "OpenAIEmbeddings-VZoxs": {},
  "Chroma-95eNk": {},
  "ChatOpenAI-Dxe2P": {},
  "CombineDocsChain-9ynVK": {},
  "RetrievalQA-xjxzD": {},
  "Data-BgRUf": {}
}


def run_flow(inputs: dict, flow_id: str, tweaks: Optional[dict] = None) -> dict:
    api_url = f"{BASE_API_URL}/{flow_id}"
    payload = {"inputs": inputs}
    if tweaks:
        payload["tweaks"] = tweaks
    response = requests.post(api_url, json=payload)
    return response.json()

def generate_response(query, filepath):
    logging.info(f"input: {query}, directory_path={filepath}")
    inputs = {"query": query, "directory_path": filepath}

    response = run_flow(inputs, flow_id=FLOW_ID, tweaks=TWEAKS)
    
    try:
        result = response.get("result", {})
        if "result" in result:
            result_text = result["result"]
            logging.info(f"answer: {result_text}")
            return result_text
        else:
            logging.error(f"Unexpected response format: {response}")
            return "Sorry, there was a problem finding an answer for you."
    except Exception as exc:
        logging.error(f"error: {exc}")
        return "Sorry, there was a problem finding an answer for you."
    




with st.sidebar:
    st.title('🤗💬 MSF ChatBot')
    st.markdown('''
    ## Upload the path.
                
    ''')


    # Upload a PDF file
    user_direc_path = st.text_input("Directory Path")

    filepath = None

    if user_direc_path:
        filepath = user_direc_path
        st.info("Path added successfully!")
        TWEAKS["Data-BgRUf"]["directory_path"] = filepath    ##  add the parameters that is to be manipulate
        # Now, TWEAKS dictionary is updated with the actual file path
        # You can proceed with further logic
    else:
        st.warning("Please upload the path of the files.")


# main chatbox
def main(): 
    st.markdown("##### Multimodal Chat App powered by 🚀 Langflow")
    st.markdown(""" <style>
        .reportview-container {
            margin-top: -2em; 
        }
        #MainMenu {visibility:hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>""", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.write(message["content"])

    if query := st.chat_input("Ask me anything..."):
        st.session_state.messages.append(
            {
                "role": "user",
                "content": query,
                "avatar": "💬",  # Emoji representation for user
            }
        )
        with st.chat_message(
            "user",
            avatar="💬",  # Emoji representation for user
        ):
            st.write(query)

        with st.chat_message(
            "assistant",
            avatar="🤖",  # Emoji representation for assistant
        ):
            message_placeholder = st.empty()
            with st.spinner(text="Thinking..."):
                assistant_response = generate_response(query, user_direc_path)
                message_placeholder.write(assistant_response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_response,
                "avatar": "🤖",  # Emoji representation for assistant
            }
        )
        


if __name__ == "__main__":
    main()  # main function execution

# -*- coding: utf-8 -*-
"""
Created on Mar 15

@author: Oyasi

@app: v0.8
"""

import logging
import sys
import time
from typing import Optional
import requests
import streamlit as st


## adding the library to upload and use document
from dotenv import load_dotenv
import os


## adding the library to use html format
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb


## adding the library to use sidebar
from streamlit_extras.add_vertical_space import add_vertical_space



log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format, stream=sys.stdout, level=logging.INFO)

BASE_API_URL = "http://localhost:7860/api/v1/process"
FLOW_ID = "eccdcbc8-8048-4d39-9c31-67c50967106d"


TWEAKS = {
  "ChatOpenAI-XSnby": {},
  "PromptTemplate-0Iw85": {},
  "PyPDFLoader-qIknj": {"file_path": "<filepath>"},
  "LLMChain-DGA6k": {}

}

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
    



# Sidebar contents
with st.sidebar:
    st.title('🤗💬 MSF ChatBot')
    st.markdown('''
    ## Upload your files here
                
    ''')


    # Upload a PDF file
    pdf_file = st.file_uploader("Upload your PDF", type='pdf')

    filepath = None

    if pdf_file:

        with open(pdf_file.name, "wb") as f:           ## bug fix : save the file in the local directory first
            f.write(pdf_file.getbuffer())

        filepath = pdf_file.name
        st.info("PDF uploaded successfully!")
        TWEAKS["PyPDFLoader-qIknj"]["file_path"] = os.path.abspath(filepath)
        # Now, TWEAKS dictionary is updated with the actual file path
        # You can proceed with further logic
    else:
        st.warning("Please upload a PDF file.")

    add_vertical_space(5)
    st.write('Sponsored ❤️ by [SHRDC](https://www.shrdc.org.my/)')
    st.markdown('\n\n\n')  # Add two blank lines using Markdown syntax


# main chatbox
def main(): 


    st.markdown("##### Multimodal Chat App powered by 🚀 Langflow")


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
                "avatar": "💬",  # Emoji representation for user
            }
        )
        with st.chat_message(
            "user",
            avatar="💬",  # Emoji representation for user
        ):
            st.write(prompt)

        with st.chat_message(
            "assistant",
            avatar="🤖",  # Emoji representation for assistant
        ):
            message_placeholder = st.empty()
            with st.spinner(text="Thinking..."):
                assistant_response = generate_response(prompt, filepath)
                message_placeholder.write(assistant_response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_response,
                "avatar": "🤖",  # Emoji representation for assistant
            }
        )




### ---------------------------------------- Footer ---------------------------------------- ###

def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(4, 4, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        "Made in ",
        image('https://avatars3.githubusercontent.com/u/45109972?s=400&v=4',
              width=px(25), height=px(25)),
        " with ❤️ by ",
        link("https://www.linkedin.com/in/oyasizakiananta/", "@Oyasi"),
    ]
    layout(*myargs)
### ---------------------------------------- Footer ---------------------------------------- ###


if __name__ == "__main__":
    main() ## main function execution 
    footer() ## footer call execution

# Conversational Retrieval QA Chatbot, built using Langflow and Streamlit
# Author: Gary A. Stafford
# Date: 2023-07-28
# Usage: streamlit run streamlit_app.py
# Requirements: pip install streamlit streamlit_chat -Uq

import logging
import sys
from typing import Optional
import requests
import streamlit as st
from streamlit_chat import message
from llm_guard import scan_output, scan_prompt
from llm_guard.input_scanners import Anonymize, PromptInjection, TokenLimit, Toxicity
from llm_guard.output_scanners import Deanonymize, NoRefusal, Relevance, Sensitive
from llm_guard.vault import Vault

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format, stream=sys.stdout, level=logging.INFO)

BASE_API_URL = "http://localhost:7860/api/v1/process"
FLOW_ID = "11014922-20a6-4400-a9af-a2f984db3943"
TWEAKS = {
    "ChatOpenAI-vlTOd": {},
    "LLMChain-Dp0f0": {},
    "ConversationBufferMemory-eM3bw": {},
    "PromptTemplate-DHzVt": {}
}

BASE_AVATAR_URL = "https://raw.githubusercontent.com/garystafford-aws/static-assets/main/static"

vault = Vault()
input_scanners = [Anonymize(vault), Toxicity(), TokenLimit(), PromptInjection()]
output_scanners = [Deanonymize(vault), NoRefusal(), Relevance(), Sensitive()]

def run_flow(inputs: dict, flow_id: str, tweaks: Optional[dict] = None) -> dict:
    api_url = f"{BASE_API_URL}/{flow_id}"

    payload = {"inputs": inputs}

    if tweaks:
        payload["tweaks"] = tweaks

    response = requests.post(api_url, json=payload)
    return response.json()

def generate_response(prompt):
    logging.info(f"question: {prompt}")
    inputs = {"Question": prompt}
    response = run_flow(inputs, flow_id=FLOW_ID, tweaks=TWEAKS)
    try:
        logging.info(f"answer: {response['result']['text']}")
        return response["result"]["text"]
    except Exception as exc:
        logging.error(f"error: {response}")
        return "Sorry, there was a problem finding an answer for you."

def main():
    st.set_page_config(page_title="Virtual Chatbox")

    st.markdown("##### Welcome to the SHRDC Q&A")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar=msg["avatar"]):
            st.write(msg["content"])

    if prompt := st.chat_input("I'm your Virtual guide, how may I help you?"):
        # Security scanning for the prompt
        sanitized_prompt, results_valid, results_score = scan_prompt(input_scanners, prompt)
        if any(results_valid.values()) is False:
            st.warning(f"Warning: The entered prompt may have security vulnerabilities. Please review your input.")
            return

        # Add user message to chat history
        st.session_state.messages.append(
            {
                "role": "user",
                "content": sanitized_prompt,
                "avatar": f"{BASE_AVATAR_URL}/people-64px.png",
            }
        )
        # Display user message in chat message container
        with st.chat_message(
            "user",
            avatar=f"{BASE_AVATAR_URL}/people-64px.png",
        ):
            st.write(sanitized_prompt)

        # Display assistant response in chat message container
        with st.chat_message(
            "assistant",
            avatar=f"{BASE_AVATAR_URL}/bartender-64px.png",
        ):
            message_placeholder = st.empty()
            with st.spinner(text="Thinking..."):
                assistant_response = generate_response(sanitized_prompt)
                # Security scanning for the response
                sanitized_response_text, results_valid, results_score = scan_output(
                    output_scanners, sanitized_prompt, assistant_response
                )
                if any(results_valid.values()) is False:
                    st.warning(f"Warning: The generated response may have security vulnerabilities. Please review the output.")
                    return
                message_placeholder.write(sanitized_response_text)
        # Add assistant response to chat history
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": sanitized_response_text,
                "avatar": f"{BASE_AVATAR_URL}/bartender-64px.png",
            }
        )

if __name__ == "__main__":
    main()

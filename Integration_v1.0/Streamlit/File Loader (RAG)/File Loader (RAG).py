import streamlit as st
import requests
import json
import logging
from typing import Optional
import os


# Load environment variables if needed

# Constants
BASE_API_URL = "http://localhost:7860"
FLOW_ID = "b827b18f-6a85-4ad3-827d-b693be2d31f6"



TWEAKS = {
  "SplitText-Dpef8": {},
  "OpenAIEmbeddings-9XRXS": {},
  "Chroma-C5Wjz": {},
  "ParseData-1i5ok": {},
  "Prompt-25ugo": {},
  "OpenAIModel-7cipj": {},
  "ChatInput-LtKTP": {},
  "ChatOutput-wqv5A": {},
  "Memory-LawNL": {},
  "File-lZLCJ": {"path": "<filepath>"}
}


# Initialize logging
logging.basicConfig(level=logging.INFO)


# Function to run the flow
def run_flow(message: str,
             endpoint: str = FLOW_ID,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             api_key: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }

    if tweaks:
        payload["tweaks"] = tweaks

    headers = {"x-api-key": api_key} if api_key else None
    response = requests.post(api_url, json=payload, headers=headers)

    # Log the response for debugging
    logging.info(f"Response Status Code: {response.status_code}")
    logging.info(f"Response Text: {response.text}")

    try:
        return response.json()
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from the server response.")
        return {}


# Function to extract the assistant's message from the response
def extract_message(response: dict) -> str:
    try:
        # Extract the response message
        return response['outputs'][0]['outputs'][0]['results']['message']['text']
    except (KeyError, IndexError):
        logging.error("No valid message found in response.")
        return "No valid message found in response."


# Streamlit App
def main():
    st.title("Langflow Chatbot 🤖")

    # Sidebar for tweaking inputs
    with st.sidebar:
        st.title('🤗💬 MSF ChatBot')
        st.markdown('''## Upload the path or enter your inputs.''')

        # Upload a PDF file
        pdf_file = st.file_uploader("Upload your PDF", type='pdf')

        filepath = None

        if pdf_file:
            # Save the uploaded file to the local directory
            with open(pdf_file.name, "wb") as f:           ## bug fix : save the file in the local directory first
                f.write(pdf_file.getbuffer())

            filepath = pdf_file.name

            st.info("PDF uploaded successfully!")
            TWEAKS["File-lZLCJ"]["path"] = os.path.abspath(filepath)  # Update tweaks with the actual file path
        else:
            st.warning("Please upload a PDF file.")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages with avatars
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.write(message["content"])

    # Input box for user message
    if query := st.chat_input("Ask me anything..."):
        # Add user message to session state
        st.session_state.messages.append(
            {
                "role": "user",
                "content": query,
                "avatar": "💬",  # Emoji for user
            }
        )
        with st.chat_message("user", avatar="💬"):  # Display user message
            st.write(query)

        # Call the Langflow API and get the assistant's response
        with st.chat_message("assistant", avatar="🤖"):  # Emoji for assistant
            message_placeholder = st.empty()  # Placeholder for assistant response
            with st.spinner("Thinking..."):
                # Fetch response from Langflow with updated TWEAKS and using `query`
                assistant_response = extract_message(run_flow(query, tweaks=TWEAKS))
                message_placeholder.write(assistant_response)

        # Add assistant response to session state
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_response,
                "avatar": "🤖",  # Emoji for assistant
            }
        )


if __name__ == "__main__":
    main()

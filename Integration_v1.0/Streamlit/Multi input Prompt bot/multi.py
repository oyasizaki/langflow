import streamlit as st
import requests
import json
import warnings
from typing import Optional

# Constants
BASE_API_URL = "http://localhost:7860"
FLOW_ID = "8a5d31ed-d2b8-4d97-835b-5cb27aea1dbc"
ENDPOINT = ""  # You can set a specific endpoint name in the flow settings
TWEAKS = {
  "Prompt-btj3T": {},
  "ChatInput-ctKfo": {},
  "OpenAIModel-SH5RG": {},
  "ChatOutput-sbVTa": {},
  "TextInput-JJNMu": {}
}

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
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if api_key:
        headers = {"x-api-key": api_key}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

# Function to extract the assistant's message from the response
def extract_message(response: dict) -> str:
    try:
        # Extract the response message
        return response['outputs'][0]['outputs'][0]['results']['message']['text']
    except (KeyError, IndexError):
        return "No valid message found in response."

# Streamlit App
def main():
    st.title("Langflow Chatbot 🤖")

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
                # Fetch response from Langflow
                assistant_response = extract_message(run_flow(query))
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

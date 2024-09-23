import streamlit as st
import requests
import json
import logging
from typing import Optional
import os


# Load environment variables if needed
# Constants for both pages
BASE_API_URL = "http://localhost:7860"
FLOW_ID_1 = "0a57ea19-f235-4770-b262-c08fa3a6a1ee"  # For file upload page
FLOW_ID_2 = "a950cd2d-fbb2-47e2-a077-1f9f59dc3a4b"  # For chatbot page

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Helper function for both flows
def run_flow(message: str,
             endpoint: str,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             api_key: Optional[str] = None) -> dict:
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

    logging.info(f"Response Status Code: {response.status_code}")
    logging.info(f"Response Text: {response.text}")

    try:
        return response.json()
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from the server response.")
        return {}

# Extract only the message text from the JSON response
def extract_message(response: dict) -> str:
    try:
        # Drill down to the relevant part of the response to get the message text
        message = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
        return message
    except (KeyError, IndexError) as e:
        logging.error(f"Error extracting message: {e}")
        return "Error: Could not extract message."

# Page 1: File Upload
def file_upload_page():
    st.title("Langflow File Upload Page 📂")

    TWEAKS = {
        "SplitText-h8RiC": {},
        "OpenAIEmbeddings-t56Du": {},
        "Chroma-0M5jb": {},
        "Directory-iJ0Rg": {"path": "<filepath>"}
    }

    # Sidebar for tweaking inputs
    with st.sidebar:
        st.title('File Upload 📁')
        st.markdown('''## Upload the path or enter your inputs.''')

        user_direc_path = st.text_input("Directory Path")

        if user_direc_path:
            filepath = user_direc_path
            st.info("Directory path provided successfully!")
            TWEAKS["Directory-iJ0Rg"]["path"] = os.path.abspath(filepath)  # Update tweaks with the actual directory path
        else:
            st.warning("Please enter a directory path.")

# Page 2: Chatbot
def chatbot_page():
    st.title("Langflow Chatbot 🤖")

    TWEAKS = {
        "Chroma-B58cX": {},
        "OpenAIEmbeddings-ivzqG": {},
        "ParseData-eartc": {},
        "Prompt-IBHUS": {},
        "OpenAIModel-Dygjp": {},
        "ChatInput-cRhcZ": {},
        "ChatOutput-3Bfl8": {},
        "Memory-tOcnI": {}
    }

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages with avatars
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.write(message["content"])

    # Input box for user message
    if query := st.chat_input("Ask me anything..."):
        st.session_state.messages.append(
            {
                "role": "user",
                "content": query,
                "avatar": "💬",
            }
        )
        with st.chat_message("user", avatar="💬"):
            st.write(query)

        # Call the Langflow API and get the assistant's response
        with st.chat_message("assistant", avatar="🤖"):
            message_placeholder = st.empty()
            with st.spinner("Thinking..."):
                # Fetch response from Langflow with updated TWEAKS and using `query`
                response = run_flow(query, endpoint=FLOW_ID_2, tweaks=TWEAKS)
                assistant_response = extract_message(response)
                message_placeholder.write(assistant_response)

        # Add assistant response to session state
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_response,
                "avatar": "🤖",
            }
        )

# Main function for switching between pages
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choose a page", ("File Upload", "Chatbot"))

    if page == "File Upload":
        file_upload_page()
    elif page == "Chatbot":
        chatbot_page()


if __name__ == "__main__":
    main()

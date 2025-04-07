from google import genai
from google.genai import types
import streamlit as st
import pandas as pd
import json
import os

# Data Loading Function
def load_data(file_path):
    try:
        if file_path.endswith(".csv"):
            return pd.read_csv(file_path)
        elif file_path.endswith(".json"):
            with open(file_path, "r") as f:
                return pd.DataFrame(json.load(f))
        elif file_path.endswith(".txt"):
            with open(file_path, "r") as f:
                return pd.DataFrame([line.strip().split("|") for line in f.readlines()])
        else:
            raise ValueError("Unsupported file format. Please use CSV, JSON, or TXT.")
    except Exception as e:
        raise ValueError(f"Error loading data: {e}. Ensure the file format matches expectations.")

# Knowledge Base Directory
KNOWLEDGE_BASE_DIR = "knowledgeBase"
os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)

# Generating Response
def generate_response(prompt, model="gemini-2.0-flash"):
    try:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

        # Flatten prompt to extract content strings
        if isinstance(prompt, list):
            prompt = [entry for entry in prompt] 

        generate_content_config = types.GenerateContentConfig(
            temperature=0.4,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="text/plain",
        )

        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=generate_content_config,
        )
        return response.text.strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Saves the uploaded file to the knowledge base directory.
def save_to_knowledge_base(uploaded_file):      
    file_path = os.path.join(KNOWLEDGE_BASE_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path    

# Main Function
def main():
    st.set_page_config(page_title="FAQ Chatbot", layout="wide")
    st.title("FAQ Chatbot")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Welcome! Please upload a CSV file so we can get started."}]
    if "history" not in st.session_state:
        st.session_state.history = [] 
    if "data" not in st.session_state:
        st.session_state.data = None  
    if "data_loaded" not in st.session_state:
        st.session_state.data_loaded = False  

    # Sidebar for session history
    with st.sidebar:
        st.header("Session History")
        if st.session_state.history:
            for idx, item in enumerate(st.session_state.history):
                st.write(f"{idx + 1}. **{item['question']}**\n\n_Response_: {item['answer']}")
        else:
            st.write("No history yet. Start a conversation!")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # File upload prompt
    uploaded_file = st.file_uploader("Upload FAQ data (CSV, JSON, or TXT)", type=["csv", "json", "txt"])

    if uploaded_file:
        try:
            # Clear previous messages and history when a new file is uploaded
            st.session_state.messages = []
            st.session_state.history = []
            st.session_state.data_loaded = False  # Reset data loaded state

            # Save the uploaded file to the knowledge base
            save_to_knowledge_base(uploaded_file)

            # Load data only once
            file_extension = uploaded_file.name.split(".")[-1]
            if file_extension == "csv":
                st.session_state.data = pd.read_csv(uploaded_file)
            elif file_extension == "json":
                st.session_state.data = pd.DataFrame(json.load(uploaded_file))
            elif file_extension == "txt":
                st.session_state.data = pd.DataFrame([line.strip().split("|") for line in uploaded_file.readlines()])
            else:
                st.error("Unsupported file type.")
                return

            st.session_state.data_loaded = True
            st.session_state.messages.append(
                {"role": "assistant", "content": f"Great! I've loaded your file: **{uploaded_file.name}**. Ask me anything about it!"}
            )
            with st.chat_message("assistant"):
                st.markdown(f"Great! I've loaded your file: **{uploaded_file.name}**. Ask me anything about it!")

            # Display FAQ data summary
            st.write("FAQ Data:")
            if len(st.session_state.data) > 100:
                st.warning("Data too large. Displaying only the first 100 rows.")
                st.dataframe(st.session_state.data.head(100))
            else:
                st.dataframe(st.session_state.data)

        except Exception as e:
            st.error(f"Error processing file: {e}")
            return

    # User input after file upload
    if st.session_state.data_loaded and (prompt := st.chat_input("Ask a question")):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display response
        faq_text = st.session_state.data.head(100).to_string(index=False)
        full_prompt = [
            f"You are a helpful FAQ answerer bot. You can answer questions from the user in a friendly manner. Rules: Answers must be brief, polite, and plain-spoken.",
            f"User 's question: {prompt}"
        ]
 
        with st.spinner("Generating response..."):
            response = generate_response(full_prompt)

        if response:
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.history.append({"question": prompt, "answer": response})  # Save to sidebar history
            with st.chat_message("assistant"):
                st.markdown(response)
        else:
            st.error("Could not generate a response. Please try again.")

if __name__ == "__main__":
    main()
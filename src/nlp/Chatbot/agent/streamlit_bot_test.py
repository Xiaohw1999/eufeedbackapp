import os
import requests
import streamlit as st

# Set chatbot URL
# CHATBOT_URL = os.getenv("CHATBOT_URL", "http://localhost:8080/query")
CHATBOT_URL = os.getenv("CHATBOT_LOCAL", "http://localhost:8000/query")
PDF_UPLOAD_URL = os.getenv("PDF_UPLOAD_URL", "http://localhost:8000/upload_pdf")

# Sidebar configuration
with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This chatbot interfaces with a FastAPI agent designed to answer questions about citizens' feedback towards EU laws and initiatives.
        """
    )

    st.header("Example Questions")
    st.markdown("- Who is the president of the USA?")
    st.markdown("- Tell me something about agriculture policy?")
    st.markdown("- Tell me the citizens' attitude towards organic food?")
    st.text("")
    st.text("")
    
    # upload PDF
    uploaded_files = st.file_uploader("Upload your PDFs", accept_multiple_files=True)

    if uploaded_files:
        with st.spinner("Uploading and processing..."):
            files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
            response = requests.post(PDF_UPLOAD_URL, files=files)
            if response.status_code == 200:
                st.success("Files uploaded and processed successfully!")
                st.session_state.pdf_processed = True
            else:
                st.error("Failed to process files.")

# Main page configuration
st.title("Civic Feedback Enhancer")
st.info("Ask me questions about EU laws, initiatives, and citizens' opinions!")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show history of chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message:
            st.markdown(message["output"])
        if "sources" in message:
            st.markdown("**Sources:**")
            for source in message["sources"]:
                st.markdown(f"- {source['text']}")
                
            
# Handle user input
if prompt := st.chat_input("What do you want to know?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"query": prompt}

    with st.spinner("Searching for an answer..."):
        try:
            response = requests.post(CHATBOT_URL, json=data)
            response.raise_for_status()
            response_json = response.json()
            output_text = response_json.get("response", "Sorry, I could not understand your question.")
            sources = response_json.get("sources", [])
        except requests.RequestException as e:
            output_text = f"An error occurred: {e}"
            sources = []

    st.chat_message("assistant").markdown(output_text)
    if sources:
        st.markdown("**Sources:**")
        for source in sources:
            st.markdown(f"- {source['text']}")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
            "sources": sources,
        }
    )

# streamlit run D:/visualstudiocode/project/eufeedbackapp/src/nlp/Chatbot/agent/streamlit_bot_test.py
# https://eu-feedback-enhancer.streamlit.app/
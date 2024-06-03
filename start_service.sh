#!/bin/bash

# Export environment variables from .env file if it exists
if [ -f .env ]; then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

# Navigate to the directory containing FastAPI app
cd src/nlp/Chatbot/chain

# Run FastAPI
uvicorn feedback_chain:app --host 0.0.0.0 --port 8000 &

# Navigate to the directory containing Streamlit app
cd ../agent

# Run Streamlit
streamlit run streamlit_bot.py --server.port 8501

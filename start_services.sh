#!/bin/bash

# start FastAPI service
nohup uvicorn src.nlp.Chatbot.chain.feedback_chain:app --host 0.0.0.0 --port 8000 &

# start Streamlit service
nohup streamlit run src/nlp/Chatbot/agent/streamlit_bot.py --server.port 8001 --server.address 0.0.0.0 &

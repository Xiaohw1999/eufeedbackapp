#!/bin/bash

# 确保终止任何现有的 Streamlit 进程
pkill -f streamlit

# 导航到项目目录
cd /mnt/d/visualstudiocode/project/eufeedbackapp || { echo "项目目录不存在"; exit 1; }

# 启动 FastAPI 服务
/mnt/d/anaconda_3/anaconda3/envs/thesis/python.exe -m uvicorn src.nlp.Chatbot.chain.feedback_chain:app --host localhost --port 8000 --reload &
FASTAPI_PID=$!

# 启动 Streamlit 服务
/mnt/d/anaconda_3/anaconda3/envs/thesis/python.exe -m streamlit run src/nlp/Chatbot/agent/streamlit_bot.py --server.port 8501 --server.address localhost &
STREAMLIT_PID=$!

# 等待所有后台进程结束
wait $FASTAPI_PID
wait $STREAMLIT_PID
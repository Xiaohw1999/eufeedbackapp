# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY .devcontainer/requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r /app/requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the necessary ports
EXPOSE 8000
EXPOSE 8501

# Run the FastAPI app with Uvicorn and Streamlit
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 & streamlit run streamlit_bot.py --server.port 8501"]
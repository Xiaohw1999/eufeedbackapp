# Use the official Python image from the Docker Hub
FROM python:3.11-bookworm

# Install sudo package
RUN apt-get update && apt-get install -y sudo

# Create vscode user with sudo privileges
RUN useradd -ms /bin/bash vscode && echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/nopasswd

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt /app/requirements.txt
COPY start_service.sh /app/start_service.sh

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r /app/requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the necessary ports
EXPOSE 8000
EXPOSE 8501

# Set the default user to vscode
USER vscode

# Run the FastAPI app with Uvicorn and Streamlit
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 & streamlit run streamlit_bot.py --server.port 8501"]
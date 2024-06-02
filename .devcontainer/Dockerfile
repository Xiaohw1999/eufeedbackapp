FROM python:3.11

# set workspace
WORKDIR /workspace

# copy requirements.txt and install dependencies
COPY requirements.txt /workspace/
RUN pip install --no-cache-dir -r /workspace/requirements.txt

# copy all files and folders
COPY . /workspace/

# expose neccessary ports
EXPOSE 8000
EXPOSE 8001
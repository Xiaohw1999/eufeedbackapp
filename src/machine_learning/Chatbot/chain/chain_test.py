import requests

api_url = "http://127.0.0.1:8000/query"
data = {"query": "Say something about the farmers"}

response = requests.post(api_url, json=data)

print(response.json())
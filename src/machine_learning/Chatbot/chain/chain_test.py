import requests

api_url = "http://127.0.0.1:8000/query"
data = {"query": "Tell me the citizens' attitude towards organic food"}

response = requests.post(api_url, json=data)

print(response.json())
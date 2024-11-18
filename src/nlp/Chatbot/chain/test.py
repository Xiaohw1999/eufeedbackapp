import requests
import json

url = "http://localhost:8000/query"  # Ensure the port number matches your server
headers = {"Content-Type": "application/json"}
data = {"query": "hello, tell me something about the food safety"}

try:
    with requests.post(url, headers=headers, json=data, stream=True, timeout=120) as response:
        response.raise_for_status()  # Check response status

        decoder = response.encoding if response.encoding else 'utf-8'

        is_answer = True
        json_buffer = ''
        end_marker = "<END_OF_ANSWER>"
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                text_chunk = chunk.decode(decoder)

                if is_answer:
                    if end_marker in text_chunk:
                        # Found the end marker
                        parts = text_chunk.split(end_marker, 1)
                        print(parts[0], end='', flush=True)  # Print the answer part

                        # Switch to collecting JSON data
                        is_answer = False

                        # Add the part after the end marker to the JSON buffer
                        json_buffer += parts[1]
                    else:
                        # End marker not found, continue printing answer
                        print(text_chunk, end='', flush=True)
                else:
                    # Collect JSON data
                    json_buffer += text_chunk

        # Parse and print JSON data
        if json_buffer.strip():
            try:
                sources = json.loads(json_buffer)
                print("\nSources:")
                for source in sources:
                    print(json.dumps(source, indent=2, ensure_ascii=False))
            except json.JSONDecodeError as e:
                print("Failed to parse JSON sources:", e)
                print("JSON buffer content:", json_buffer)
except requests.exceptions.Timeout:
    print("Request timed out. Please try again.")
except requests.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

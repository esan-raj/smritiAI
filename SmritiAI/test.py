import requests

url = "http://localhost:7860/api/v1/flows"

response = requests.get(url)

if response.status_code == 200:
    print("✅ Langflow API is working!")
    print(response.json())  # Print available flows
else:
    print(f"⚠️ Error: {response.status_code} - {response.text}")

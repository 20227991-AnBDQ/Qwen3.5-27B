import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"prompt": "Xin chào"}
)

print(response.status_code)
print(response.json())

import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"prompt": "Xin chào"}
)

print("Status:", response.status_code)
print("Response:", response.json())

# Debug: Test Ollama trực tiếp
ollama_response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "qwen:4b", "prompt": "Xin chào", "stream": False}
)
print("Ollama Status:", ollama_response.status_code)
print("Ollama Response:", ollama_response.json())

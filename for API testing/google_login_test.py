import requests

url = "http://127.0.0.1:8000/api/users/login-google/"
data = {
    "token": "TOKEN"
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json() if response.content else "No content")

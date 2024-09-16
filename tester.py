import requests

url = "http://127.0.0.1:8000/api/students/libraries"
headers = {
    'Authorization': "a0629a1a912a8c29122b721ba640529c3ee50534"
}
response = requests.get(url, headers=headers)

print(response.json())
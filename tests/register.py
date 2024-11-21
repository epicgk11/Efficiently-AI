import requests

headers = {
    'userId':"asdsasaasdsadfsaqw",
}

response = requests.post('http://127.0.0.1:8000/data/register/',headers=headers)

print(response.json())
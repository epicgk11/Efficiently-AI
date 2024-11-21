import requests

headers = {
    "Content-Type": "application/json",
    "userId": "asdsasaasdsadfsaqw"
}

res = requests.get(
            "http://localhost:8000/data/tasks/",
            headers = headers
            )

print(res.json())
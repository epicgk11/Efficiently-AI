import requests

headers = {
    "Content-Type": "application/json",
    "userId": "asdsasaasdsadfsaqw"
}

res = requests.post(
            "http://localhost:8000/data/tasks/673f87b26b7d8fd9b21da76f/",
            headers = headers
            )

print(res.json())
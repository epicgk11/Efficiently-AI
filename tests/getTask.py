import requests

headers = {
    "Content-Type": "application/json",
    "userId": "harisankar1603@gmail.com"
}

res = requests.get(
            "http://localhost:8000/data/v2/tasks/67454daee656fc1135741440/",
            headers = headers
            )

print(res.json())
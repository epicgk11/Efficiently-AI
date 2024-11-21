task_id = "673f7a21c62975c49ddca1e0"
import requests

headers = {
    "Content-Type": "application/json",
    "userId": "asdsasaasdsadfsaqw"
}

res = requests.delete(
            "http://localhost:8000/data/tasks/delete/673f7a21c62975c49ddca1e0/",
            headers = headers
            )

print(res.json())
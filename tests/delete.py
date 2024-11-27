task_id = "673f7a21c62975c49ddca1e0"
import requests

headers = {
    "Content-Type": "application/json",
    "userId": "sample"
}

res = requests.delete(
            "http://localhost:8000/data/v2/tasks/6747489b2a1d39e11789f94d/",
            headers = headers
            )

print(res.json())
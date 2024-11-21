task_id = "673f7c17806b4fdb5013583b"
import requests
import json

task_data = {
    "name": "Complete Project Report",
    "description": "Work on the project report for the AI course.",
    "due_date": "2024-11-30",
    "tags": ["work", "urgent"],
    "steps": [
        {"name": "Draft the introduction", "completed": False, "due_date": "2024-11-25"},
        {"name": "Draft the introdion", "completed": False, "due_date": "2024-11-24"}
    ]
}

headers = {
    "Content-Type": "application/json",
    "userId": "asdsasaasdsadfsaqw"
}

res = requests.post(
            "http://localhost:8000/data/tasks/update/673f7a21c62975c49ddca1e0/",
            data = json.dumps(task_data),
            headers = headers
            )

print(res.json())
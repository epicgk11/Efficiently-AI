import requests
import json

dummy_encrypted_id = "asdsasaasdsadfsaqw"

url = "http://localhost:8000/data/tasks/create/"

task_data = {
    "name": "Complete Project Report",
    "description": "Work on the project report for the AI course.",
    "due_date": "2024-11-30",
    "tags": ["work", "urgent",'asdas'],
    "steps": [
        {"name": "Draft the introduction", "completed": False, "due_date": "2024-11-25"},
        {"name": "Prepare the summary", "completed": False, "due_date": "2024-11-28"}
    ]
}

headers = {
    "Content-Type": "application/json",
    "userId": dummy_encrypted_id
}

response = requests.post(url, data=json.dumps(task_data), headers=headers)

print("Status Code:", response.status_code)
print("Response Body:", response.json())

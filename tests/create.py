import requests
import json


url = "http://localhost:8000/data/v2/tasks/create/"

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
    "userId": "sample"
}

response = requests.post(url, data=json.dumps(task_data), headers=headers)

print("Status Code:", response.status_code)
print("Response Body:", response.json())

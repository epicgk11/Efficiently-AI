import requests
import json

# Replace with your actual API base URL
API_BASE_URL = 'http://localhost:8000'

# Endpoints
REGISTER_URL = f'{API_BASE_URL}/register/'
LOGIN_URL = f'{API_BASE_URL}/login/'
CREATE_TASK_URL = f'{API_BASE_URL}/createTask/'
LIST_TASKS_URL = f'{API_BASE_URL}/listTasks/'
GET_TASK_URL = f'{API_BASE_URL}/getTask/{{task_id}}/'
UPDATE_TASK_URL = f'{API_BASE_URL}/updateTask/{{task_id}}/'
DELETE_TASK_URL = f'{API_BASE_URL}/deleteTask/{{task_id}}/'

# Test User Data
user_data = {
    "email": "testuser@example.com",
    "username": "testuser",
    "password1": "securepassword123",
    "password2": "securepassword123"
}

# Session to persist cookies
session = requests.Session()

def register_user():
    print("Registering user...")
    response = session.post(REGISTER_URL, data=user_data)
    if response.status_code == 200:
        data = response.json()
        encrypted_id = data.get('encrypted_id')
        print(f"User registered. Encrypted ID: {encrypted_id}")
        return encrypted_id
    else:
        print(f"Registration failed: {response.text}")
        return None

def login_user():
    print("Logging in user...")
    login_data = {
        "username": user_data['email'],  # Assuming login with email
        "password": user_data['password1']
    }
    response = session.post(LOGIN_URL, data=login_data)
    if response.status_code == 200:
        print("User logged in successfully.")
        return True
    else:
        print(f"Login failed: {response.text}")
        return False

def create_task(encrypted_id):
    print("Creating a new task...")
    headers = {
        'Encrypted-ID': encrypted_id,
        'Content-Type': 'application/json'
    }
    task_data = {
        "name": "Finish Assignment",
        "description": "Complete the math assignment before due date",
        "due_date": "2024-11-30",
        "tags": ["school", "urgent"],
        "resources": "Notebook, Calculator",
        "steps": [
            {"name": "Solve equations", "due_date": "2024-11-25", "completed": False},
            {"name": "Check answers", "due_date": "2024-11-27", "completed": False}
        ]
    }
    response = session.post(CREATE_TASK_URL, headers=headers, json=task_data)
    if response.status_code == 200:
        data = response.json()
        task_id = data.get('task_id')
        print(f"Task created. Task ID: {task_id}")
        return task_id
    else:
        print(f"Failed to create task: {response.text}")
        return None

def list_tasks(encrypted_id):
    print("Listing all tasks...")
    headers = {
        'Encrypted-ID': encrypted_id
    }
    response = session.get(LIST_TASKS_URL, headers=headers)
    if response.status_code == 200:
        tasks = response.json().get('tasks', [])
        print(f"Retrieved {len(tasks)} tasks.")
        print(json.dumps(tasks, indent=2))
    else:
        print(f"Failed to list tasks: {response.text}")

def get_task(encrypted_id, task_id):
    print(f"Getting task {task_id}...")
    headers = {
        'Encrypted-ID': encrypted_id
    }
    url = GET_TASK_URL.format(task_id=task_id)
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        task = response.json().get('task', {})
        print("Task details:")
        print(json.dumps(task, indent=2))
    else:
        print(f"Failed to get task: {response.text}")

def update_task(encrypted_id, task_id):
    print(f"Updating task {task_id}...")
    headers = {
        'Encrypted-ID': encrypted_id,
        'Content-Type': 'application/json'
    }
    updated_task_data = {
        "name": "Finish Assignment - Updated",
        "description": "Complete the assignment with final review",
        "due_date": "2024-12-01",
        "tags": ["school", "review"],
        "resources": "Notebook, Calculator, Pen",
        "steps": [
            {"name": "Solve equations", "due_date": "2024-11-25", "completed": True},
            {"name": "Check answers", "due_date": "2024-11-30", "completed": False}
        ]
    }
    url = UPDATE_TASK_URL.format(task_id=task_id)
    response = session.post(url, headers=headers, json=updated_task_data)
    if response.status_code == 200:
        print("Task updated successfully.")
    else:
        print(f"Failed to update task: {response.text}")

def delete_task(encrypted_id, task_id):
    print(f"Deleting task {task_id}...")
    headers = {
        'Encrypted-ID': encrypted_id
    }
    url = DELETE_TASK_URL.format(task_id=task_id)
    response = session.delete(url, headers=headers)
    if response.status_code == 200:
        print("Task deleted successfully.")
    else:
        print(f"Failed to delete task: {response.text}")

def main():
    # Step 1: Register User and Get Encrypted ID
    encrypted_id = register_user()
    if not encrypted_id:
        return

    # Step 2: Log in User (if your system requires login to set session cookies)
    login_success = login_user()
    if not login_success:
        return

    # Step 3: Create a Task
    task_id = create_task(encrypted_id)
    if not task_id:
        return

    # Step 4: List Tasks
    list_tasks(encrypted_id)

    # Step 5: Get Specific Task
    get_task(encrypted_id, task_id)

    # Step 6: Update Task
    update_task(encrypted_id, task_id)

    # Step 7: Get Updated Task
    get_task(encrypted_id, task_id)

    # Step 8: Delete Task
    delete_task(encrypted_id, task_id)

    # Step 9: List Tasks to Confirm Deletion
    list_tasks(encrypted_id)

if __name__ == "__main__":
    main()

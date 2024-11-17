import json
import re

def parseTaskDataFromRequest(request):
    # Parse data from the request
    if request.headers.get('Content-Type') == 'application/json':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = {}
    else:
        data = request.POST.copy()

    # Extract basic task information
    task_name = data.get('name')
    task_description = data.get('description')
    task_due_date = data.get('due_date')
    task_resources = data.get('resources', '')
    
    # Process tags
    print(data)
    task_tags = data.get('tags', '')
    print("tags are ",task_tags)
    if isinstance(task_tags, str):
        task_tags = task_tags.split(',')
    elif isinstance(task_tags, list):
        task_tags = task_tags
    else:
        task_tags = []
    task_tags = [tag.strip() for tag in task_tags if tag.strip()]

    # Determine completion status
    completed = data.get('completed', 'off')
    if isinstance(completed, str):
        completed = completed.lower() in ['on', 'true']
    else:
        completed = bool(completed)

    # Process steps
    steps = []
    if 'steps' in data and isinstance(data['steps'], list):
        steps = data['steps']
        for step in steps:
            step_completed = step.get('completed', 'off')
            if isinstance(step_completed, str):
                step['completed'] = step_completed.lower() in ['on', 'true']
            else:
                step['completed'] = bool(step_completed)
    else:
        step_dict = {}
        for key in data.keys():
            if key.startswith('step-'):
                match = re.match(r'step-(\d+)-(.+)', key)
                if match:
                    index = int(match.group(1))
                    field = match.group(2)
                    step_dict.setdefault(index, {})[field] = data[key]
        for index in sorted(step_dict.keys()):
            step = step_dict[index]
            step_completed = step.get('completed', 'off')
            if isinstance(step_completed, str):
                step['completed'] = step_completed.lower() in ['on', 'true']
            else:
                step['completed'] = bool(step_completed)
            steps.append(step)

    # Construct the task dictionary
    task_dict = {
        'name': task_name,
        'description': task_description,
        'due_date': task_due_date,
        'resources': task_resources,
        'completed': completed,
        'steps': steps,
        'tags': task_tags,
    }

    return task_dict

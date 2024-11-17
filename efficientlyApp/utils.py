import json

def handlechecks(checklist):
    i = 0
    return_list = []
    while(i<len(checklist)):
        if(i+1<len(checklist) and checklist[i+1]=="1"):
            return_list.append(True)
            i+=2
        else:
            return_list.append(False)
            i+=1
    return return_list

def parse(request):
    name = request.POST.get('name')
    description = request.POST.get('description')
    due_date = request.POST.get('due_date')
    tags = request.POST.get('tags').split(",")
    resources = request.POST.get('resources')
    step_names = request.POST.getlist('step_name[]')
    step_due_dates = request.POST.getlist('step_due_date[]')
    step_completed = request.POST.getlist('step_completed[]')
    step_completed = handlechecks(step_completed)
    steps = []
    for i in range(len(step_names)):
        completed = step_completed[i]
        steps.append({
            'name': step_names[i],
            'due_date': step_due_dates[i],
            'completed': completed
        })
    task_data = {
        "name": name,
        "description": description,
        "due_date": due_date,
        "tags": tags,
        "resources": resources,
        "steps": steps
    }
    return task_data
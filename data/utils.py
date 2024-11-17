from .mongoUtils import MongoDB

mongo = MongoDB()
tasksCollections = mongo.getCollection('tasks')

def createTask(data):
    taskId = tasksCollections.insert_one(data).inserted_id
    return taskId

def updateTask(taskId,updates):
    tasksCollections.update_one({"_id":taskId},{"$set":updates})

def deleteTask(taskId):
    tasksCollections.delete_one({"_id":taskId})

def getTask(taskId):
    task = tasksCollections.find_one({"_id":taskId})
    task['id'] = str(task.pop("_id"))
    return task

def listTasks():
    tasks = list(tasksCollections.find())
    for task in tasks:
        task['id'] = str(task.pop("_id"))
    return tasks                                          
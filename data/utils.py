from .mongoUtils import MongoDB
from bson.objectid import ObjectId
mongo = MongoDB()
usersCollection = mongo.getCollection('users')

print(usersCollection)

def createUser(data):
    data['tasks']=[]
    user_id = usersCollection.insert_one(data).inserted_id
    return user_id

def addTaskToUser(userId, task):
    print(userId)
    user = usersCollection.find({'userId': userId})
    print(user)
    if user:
        task['_id'] = str(ObjectId())
        result = usersCollection.update_one({'userId': userId}, {'$push': {'tasks': task}})
        return task

def updateUserTask(userId, task_id, updates):
    user = usersCollection.find_one({'userId': userId})
    if user:
        tasks = user.get('tasks', [])
        for task in tasks:
            if task['_id'] == task_id:
                task.update(updates)
                break
        usersCollection.update_one({'userId': userId}, {'$set': {'tasks': tasks}})

def deleteUserTask(userId, task_id):
    user = usersCollection.find_one({'userId': userId})
    if user:
        tasks = [task for task in user['tasks'] if task['_id'] != task_id]
        usersCollection.update_one({'userId': userId}, {'$set': {'tasks': tasks}})

def getUserTasks(userId):
    user = usersCollection.find_one({'userId': userId})
    return user.get('tasks', []) if user else []

def getSpeceficTask(userId,taskId):
    user = usersCollection.find_one({'userId':userId})
    if user:
        for task in user['tasks']:
            if task['_id'] == taskId:
                return task
    return {"message":"Task Not Found"}

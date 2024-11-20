from .mongoUtils import MongoDB
from bson.objectid import ObjectId
mongo = MongoDB()
usersCollection = mongo.getCollection('users')

print(usersCollection)

def createUser(data):
    data['tasks']=[]
    user_id = usersCollection.insert_one(data).inserted_id
    return user_id

def addTaskToUser(encrypted_id, task):
    print(encrypted_id)
    user = usersCollection.find({'Encrypted-ID': encrypted_id})
    print(user)
    if user:
        task['_id'] = str(ObjectId())
        result = usersCollection.update_one({'Encrypted-ID': encrypted_id}, {'$push': {'tasks': task}})
        return task

def updateUserTask(encrypted_id, task_id, updates):
    user = usersCollection.find_one({'Encrypted-ID': encrypted_id})
    if user:
        tasks = user.get('tasks', [])
        for task in tasks:
            if task['_id'] == task_id:
                task.update(updates)
                break
        usersCollection.update_one({'Encrypted-Id': encrypted_id}, {'$set': {'tasks': tasks}})

def deleteUserTask(encrypted_id, task_id):
    user = usersCollection.find_one({'Encrypted-ID': encrypted_id})
    if user:
        tasks = [task for task in user['tasks'] if task['_id'] != task_id]
        usersCollection.update_one({'Encrypted-ID': encrypted_id}, {'$set': {'tasks': tasks}})

def getUserTasks(encrypted_id):
    user = usersCollection.find_one({'Encrypted-ID': encrypted_id})
    return user.get('tasks', []) if user else []

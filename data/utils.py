from .mongoUtils import MongoDB
from bson.objectid import ObjectId
mongo = MongoDB()
usersCollection = mongo.getCollection('users')

def createUser(data):
    data['tasks']=[]
    data['bio']=None
    data['profilePic'] = None
    data['commitments'] = []
    user_id = usersCollection.insert_one(data).inserted_id
    return user_id

def addAdditionalInfo(userId, data):
    user = usersCollection.find_one({'userId': userId})
    if user:
        bio = data.get('bio')
        profilePic = data.get('profilePic')
        new_commitments = data.get('commitments', [])
        update_fields = {}
        if bio is not None:
            update_fields['bio'] = bio
        if profilePic is not None:
            update_fields['profilePic'] = profilePic
        if new_commitments:
            update_fields['commitments'] = new_commitments
        result = usersCollection.update_one(
            {'userId': userId},
            {'$set': update_fields}
        )
        
        return {'matched': result.matched_count, 'modified': result.modified_count}
    else:
        return {'error': 'User not found'}
    
def getAdditionalInfo(userId):
    user = usersCollection.find_one({'userId': userId})
    return {
        'bio':user.get('bio',None),
        'image bytes':user.get('profilePic',None),
        'commitments':user.get('commitments',[])
    }

def getProfilePic(userId):
    user = usersCollection.find_one({'userId': userId})
    return user.get('profilePic',None)


def addTaskToUser(userId, task):
    user = usersCollection.find({'userId': userId})
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
                return {'task':task}
    return {"message":"Task Not Found"}

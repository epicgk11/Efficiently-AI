from pymongo import MongoClient
from django.conf import settings

class MongoDB:
    def __init__(self):
        self.client = MongoClient(
            host=settings.MONGO_DB['HOST'],
            port=settings.MONGO_DB['PORT'],
            serverSelectionTimeoutMS=2000,
        )
        self.db = self.client[settings.MONGO_DB['NAME']]

    def getCollection(self, collection_name):
        return self.db[collection_name]

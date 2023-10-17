import configparser
import pymongo
from bson.objectid import ObjectId

config = configparser.ConfigParser()
config.read("./conf.conf")


class BaseDBError(Exception):
    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    __str__ = __repr__


class IDOverlapping(BaseDBError):
    pass


class IllegalStatus(BaseDBError):
    pass


class DocumentNotFound(BaseDBError):
    pass


class DBHandler:
    def __init__(self):
        self.client = pymongo.MongoClient(f"mongodb://{config['DB']['ServerAddr']}:{config['DB']['ServerPort']}")
        self.db = self.client[config['DB']['ID']]
        self.collection = self.db[config['DB']['collection']]

    def insert_data(self, data):
        # existing = self.get_data_by_id(data.get(id))
        # if existing:
        #     raise IDOverlapping(f"{data}: id 중복됨")
        return self.collection.insert_one(data)

    def get_data_by_id(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})

    def fetch_all(self):
        return self.collection.count_documents({}), self.collection.find({})

    def get_datas_by_name(self, client_name):
        return self.collection.find({"data.CustomerName": client_name})

    def update_status_by_id(self, id, new_status):
        if new_status not in ["waiting", "done", "inprogress", "error"]:
            raise IllegalStatus(str(new_status))

        self.collection.update_one({"_id": ObjectId(id)}, {"$set": {"status": new_status}})

    def update_assigned_by_id(self, id, new_assigned_value):
        if str(new_assigned_value) not in ["0", "1", "2"]:
            raise IllegalStatus(str(new_assigned_value))
        self.collection.update_one({"_id": ObjectId(id)}, {"$set": {"assignedAt": str(new_assigned_value)}})

    def update_color_by_id(self, id, new_color):
        self.collection.update_one({"_id": ObjectId(id)}, {"$set": {"data.ColorCode": new_color}})

    def delete_data_by_id(self, id):
        self.collection.delete_one({"_id": ObjectId(id)})

    def close(self):
        self.client.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

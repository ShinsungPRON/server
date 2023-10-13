import configparser
import pymongo

config = configparser.ConfigParser()
config.read("./conf.conf")


class BaseDBError(Exception):
    """Base class for ConfigParser exceptions."""

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
        existing = self.find_data(data.get("id"))
        if existing:
            raise IDOverlapping(f"{data}: id 중복됨")

        return self.collection.insert_one(data)

    def get_data(self, id):
        return self.collection.find_one({"id": id})

    def update_status(self, id, new_status):
        if not new_status in ["waiting", "done", "inprogress"]:
            raise IllegalStatus(str(new_status))

        self.collection.update_one({"id": id}, {"$set": {"status": new_status}})

    def update_color(self, id, new_color):
        self.collection.update_one({"id": id}, {"$set": {"data.ColorCode": new_color}})

    def delete_data(self, id):
        self.collection.delete_one({"id": id})

    def close(self):
        self.client.close()
import configparser
import pymongo

config = configparser.ConfigParser()
config.read("./conf.conf")

class DBHandler:
    def __init__(self):
        self.client = pymongo.MongoClient(f"mongodb://{config['DEFAULT']['ServerAddr']}:{config['DEFAULT']['ServerPort']}")
        self.db = self.client[config['DB']['ID']]
        self.collection = self.db[config['DB']['collection']]

    def insert_data(self, data):
        existing = self.find_data(data.get("id"))
        if existing:
            return print("! | id 중복됨 (db반영X) \n")

        return self.collection.insert_one(data)

    def get_data(self, id):
        return self.collection.find_one({"id": id})

    def update_status(self, id, new_status):
        self.collection.update_one({"id": id}, {"$set": {"status": new_status}})

    def update_color(self, id, new_color):
        self.collection.update_one({"id": id}, {"$set": {"data.ColorCode": new_color}})

    def delete_data(self, id):
        self.collection.delete_one({"id": id})

    def close(self):
        self.client.close()
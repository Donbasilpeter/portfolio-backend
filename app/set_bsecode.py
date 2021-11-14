import pymongo
from pymongo import MongoClient


if __name__ == "app.set_bsecode":
    import json
    with open("app/data.json", 'r') as data_file:
        json_data = data_file.read()
    data = json.loads(json_data)


    client = MongoClient("database",27017)
    db = client.portfolio_app
    db.bsecode.remove()

    collection = db.bsecode

    for codes in data:
        print(codes)
        collection.insert_one(codes)
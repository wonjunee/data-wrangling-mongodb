"""
MongoDB insert script for final project.
Database: finalproject
Collection: map

import from map.json
"""

import json

def insert_line(line, db):
    db.map.insert(line)

""" open map.json file and put data into MongoDB """
def insert_to_mongodb(filename, db):
    with open(filename) as f:
        for line in f:
            data = json.loads(line)
            insert_line(data,db)

if __name__ == "__main__":
    
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    client.drop_database("finalproject")
    db = client.finalproject

    insert_to_mongodb('c:/map.json', db)
    print db.map.find_one()
    print db.map.count() # 398663
    
    assert db.map.count() == 398663

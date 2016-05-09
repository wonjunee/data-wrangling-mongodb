"""
Complete the insert_data function to insert the data into MongoDB.
"""

import json
import pprint
def insert_data(data, db):
    db.tweets.insert(data)


if __name__ == "__main__":
    
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.twitter
    print client.database_names()
    tweets = []
    # with open('c:/twitter.json') as f:
    # 	for line in f:
    # 		db.tweets.insert(json.loads(line))

        # pprint.pprint(tweets[0])
        # data = json.loads(f.read())
        # insert_data(tweets, db)
        # print db.tweets.find_one()
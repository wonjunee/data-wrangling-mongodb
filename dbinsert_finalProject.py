"""
Complete the insert_data function to insert the data into MongoDB.
"""

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

def insert_data(data, db):
    db.tweets.insert(data)


if __name__ == "__main__":
    
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.project
    print client.database_names()
    data = []
    # with open('c:/project.json') as f:
    # 	for line in f:
    # 		db.tweets.insert(json.loads(line))

    #     pprint.pprint(tweets[0])
    #     data = json.loads(f.read())
    #     insert_data(tweets, db)
    #     print db.tweets.find_one()

    # with codecs.open('c:/chicago.json', "w") as fo:
    #     for _, element in ET.iterparse(file_in):
    #         el = shape_element(element)
    #         if el:
    #             data.append(el)
    #             if pretty:
    #                 fo.write(json.dumps(el, indent=2)+"\n")
    #             else:
    #                 fo.write(json.dumps(el) + "\n")

    with open("c:/map") as F:
        # for line in F:
        #     db.map.insert(line)
        for _, element in ET.iterparse("c:/map"):
            db.map.insert(element)
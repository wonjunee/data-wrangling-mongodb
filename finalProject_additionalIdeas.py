#!/usr/bin/env python
# Run this after "finalProject_dbinsert.py"

import pprint

def get_db(db_name):
    """ Import Database """
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

if __name__ == '__main__':
    db = get_db('finalproject')

    # list the colletion names
    print db.collection_names()
    print db.building.count()

    result = db.map.aggregate([
            {
            "$match": {
                    "$or":
                    [
                    {"building": "apartments"},
                    {"building": "residential"},
                    {"building": "house"},
                    {"building": "Townhouse"}
                    ]
                }
            },
            {
            "$project": {"node": "$node_refs"}
            }
        ])
    # for i in result:
    #     pprint.pprint(i)

    print db.building.find_one()
    # for i in result:
    #     pprint.pprint(i)


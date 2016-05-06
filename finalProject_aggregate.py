#!/usr/bin/env python
import pprint

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [
        {"$match" : {"name" : {"$ne" : None },
                     "lon" : {"$gt" : 75, "$lt" : 80 } } },
        {"$unwind" : "$isPartOf"},
        # {"$group" : {"_id" : "$isPartOf", "list" : {"$addToSet" : "$name"} } },
        # {"$unwind" : "$list" },
        {"$group" : {"_id" : "$isPartOf",
                     "count" : {"$sum" : 1} } },
        {"$sort" : {"count" : -1 } },
        {"$limit" : 1 }
        ]
    return pipeline

def aggregate(db, pipeline):
    return [doc for doc in db.map.aggregate(pipeline)]

if __name__ == '__main__':
    db = get_db('finalproject')

    """ Total Count """
    print "Total Number of Records:", db.map.count()

    """ Total node numbers """
    print "Total Number of Nodes:", db.map.find({"type":"node"}).count()

    """ Total way numbers """
    print "Total Number of Ways:", db.map.find({"type":"way"}).count()

    """ Total number of unique users """
    print "Total Number of Unique Users:", len(db.map.distinct("created.user"))

    """ Total number of unique sources """
    unique_sources = db.map.distinct("created.source")
    print "Total Number of Unique Sources:", len(unique_sources)
    pprint.pprint(unique_sources)

    """ Fix sources """
    fix_sources = {"Bing"  : ["binng", "BING", "bing", "bing imagery", "Bing imagery", "bing imagery, _data,firld papers,on-site", "biung", "Bing, site visit"],
                   "Yahoo" : ["Yahoo imagery", "yahoo"],
                   "site visit" : ["Site visit", "imagery", "site survey", "GPS, site visit"],
                   "ground trugh" : ["ground truthing"],
                   "fairfaxtrails.org" : ['http://www.fairfaxtrails.org', 'http://www.fairfaxtrails.org/pimmit/110707Legal_brochures_updown.pdf'],
                   "Fairfax County GIS" : ['Fairfax County Free GIS data','www.fairfaxcounty.gov > Tax Records property map 0602010037','Fairfax County GIS (http://www.fairfaxcounty.gov/maps/metadata.htm)','county_import_v0.1_20080508235459'],
                   "knowledge" : ['ground truth','I work there','local knowledge','In-person Source, ate there'],
                   "survey" : ["ground survey"],
                   "Tiger" : ['TIGER/Line 2008 Place Shapefiles (http://www.census.gov/geo/www/tiger/)', "Tiger2008 by DaleP 2009-02-28"]
                }

    for key in fix_sources.keys():
        for word in fix_sources[key]:
            db.map.update(
                        { "created.source" : word},
                        { "$set": {
                            "created.source" : key
                            }
                        },
                        multi = True
                    )
    unique_sources = db.map.distinct("created.source")
    print "After processing"
    print "Total Number of Unique Sources:", len(unique_sources)
    pprint.pprint(unique_sources)

    """ Top contributing users """
    top_user = db.map.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":5}])
    print "Top 5 Contributing Users"
    for doc in top_user:
        print doc

    """ Top source """
    top_source = db.map.aggregate([{"$group":{"_id":"$created.source", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":5}])
    print "Top 5 Sources"
    for doc in top_source:
        print doc

    """ Number of users appearing only once """
    one_time_users = db.map.aggregate([ {
                                        "$group": {
                                            "_id": "$created.user",
                                            "count": { "$sum" : 1}
                                            }
                                        },
                                        {
                                        "$match": {
                                            "count" : 1
                                            }
                                        }
                                    ])
    count = 0
    one_time_users_list = []
    for user in one_time_users:
        one_time_users_list.append(user)
        count += 1

    print "Number of One Time Users:", count

    """ Top user for each source """
    for source in unique_sources:
        source_top_user = db.map.aggregate([ {
                "$match": { "created.source" : source },
                },
                {
                "$group": {
                    "_id": "$created.user",
                    "count": { "$sum" : 1}
                    }
                },
                {
                "$sort": {"count": -1}
                },
                {
                "$limit": 1
                }
            ])
        top_user = [doc for doc in source_top_user]
        print "Top User of", source,":", top_user[0]['_id'], "-", top_user[0]["count"]
    
    """ Number of buildings """
    num_building = db.map.aggregate([{
            "$match": {"building": {"$ne" : None}}
            },
            {
            "$limit": 10
            }
        ])
    for doc in num_building:
        print doc
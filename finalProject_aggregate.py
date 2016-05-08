#!/usr/bin/env python
# Run this after "finalProject_dbinsert.py"

import pprint

def get_db(db_name):
    """ Import Database """
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def fix_source(db):
    """ Fix sources """
    fix_sources = {"Bing"  : ['Bing; knowledge; logic','bing imagery,_data, field papers,on-site','bing imagery,_data,field papers,on-site',"binng", "BING", "bing", "bing imagery", "Bing imagery", "bing imagery, _data,firld papers,on-site", 'bing imagery, _data, field papers, on-site', "biung", "Bing, site visit"],
                   "Yahoo" : ["Yahoo imagery", "yahoo"],
                   "site visit" : ["Site visit", "imagery", "site survey", "GPS, site visit"],
                   "ground truth" : ["ground truthing"],
                   "fairfaxtrails.org" : ['http://www.fairfaxtrails.org', 'http://www.fairfaxtrails.org/pimmit/110707Legal_brochures_updown.pdf'],
                   "Fairfax County GIS" : ['http://www.fairfaxcounty.gov/library/branches/dm/','Fairfax County Free GIS data','www.fairfaxcounty.gov > Tax Records property map 0602010037','Fairfax County GIS (http://www.fairfaxcounty.gov/maps/metadata.htm)','county_import_v0.1_20080508235459'],
                   "knowledge" : ['from walking it','ground truth','I work there','local knowledge','In-person Source, ate there'],
                   "survey" : ["ground survey"],
                   "Tiger" : ['TIGER/Line 2008 Place Shapefiles (http://www.census.gov/geo/www/tiger/)', "Tiger2008 by DaleP 2009-02-28"],
                   "DCGIS" : ['DCGIS; NPS','DCGIS; NPS; Park Service Map; USGS NM',"dcgis"]
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
    return unique_sources

if __name__ == '__main__':
    db = get_db('finalproject')

    """ Total Count """
    print "\nTotal Number of Records:", db.map.count()

    """ Total node numbers """
    print "\nTotal Number of Nodes:", db.map.find({"type":"node"}).count()

    """ Total way numbers """
    print "\nTotal Number of Ways:", db.map.find({"type":"way"}).count()

    """ Total number of unique users """
    print "\nTotal Number of Unique Users:", len(db.map.distinct("created.user"))

    """ Total number of unique sources """
    unique_sources = db.map.distinct("created.source")
    print "\nTotal Number of Unique Sources:", len(unique_sources)
    pprint.pprint(unique_sources)


    """ Fix Sources """
    # unique_sources = fix_source(db)

    """ Top contributing users """
    top_user = db.map.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":5}])
    print "\nTop 5 Contributing Users"
    for doc in top_user:
        print doc

    """ Top source """
    top_source = db.map.aggregate([{"$group":{"_id":"$created.source", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":5}])
    print "\nTop 5 Sources"
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

    print "\nNumber of One Time Users:", count

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


    """ Amenities """
    num_metros = db.map.aggregate([
            {
            "$match": {"amenity": {"$ne": None}}
            },
            {
            "$group": {"_id": "$amenity", "count": {"$sum": 1}}
            },
            {
            "$sort" : {"count": -1}
            },
            {
            "$limit": 5
            }
        ])

    print "\nTop 5 Amenities"
    for i in num_metros:
        print i

    # Actually there are more than 3 but looks like the data is not up-to-date.


    """ Number of Amenities """
    num_metros = db.map.aggregate([
            {
            "$match": {"amenity": {"$ne": None}}
            },
            {
            "$group": {"_id": "$amenity"}
            },
            {
            "$group": {"_id": None, "count": {"$sum": 1}}
            }
        ])
    for i in num_metros:
        print "\nNumber of Amenities:", i["count"]

    """ Number of Amenities """
    num_metros = db.map.aggregate([
            {
            "$match": {"amenity": {"$ne": None}}
            },
            {
            "$group": {"_id": None, "count": {"$sum": 1}}
            }
        ])
    for i in num_metros:
        print "\nNumber of Amenities Exists in The Data:", i["count"]

    """ Number of Schools """
    num_metros = db.map.aggregate([
            {
            "$match": {"amenity": "school"}
            },
            {
            "$group": {"_id": None, "count":{"$sum":1}}
            }
        ])
    for i in num_metros:
        print "\nNumber of Schools:", i["count"]

    """ Number of Buildings """
    num_metros = db.map.aggregate([
            {
            "$match": {"building": {"$ne": None}}
            },
            {
            "$group": {"_id": None, "count":{"$sum": 1}}
            }
        ])
    for i in num_metros:
        print "\nNumber of Buildings:", i["count"]

    # ADDITIONAL STATISTICS
    # 1. Percentage of top source
    # 2. Percentage of top user
    # 3. Percentage of top amenity
    # 4. Percentage of top building

    """ Percentage of top source """
    top_source_percentage = 394065.0/398663.0*100
    second_source_percentage = 3385.0/398663.0*100
    print "\nPercentage of top source (None):", top_source_percentage, "%"
    print "\nPercentage of 2nd top source (Bing)", second_source_percentage, "%"

    """ Percentage of top user """
    print "\nPercentage of top user (ingalls):", (133558.0/398663.0*100), "%"

    """ Percentage of top amenity """
    print "\nPercentage of top amenity (restaurant)", (173.0/872.0*100), "%"

    # ADDITIONAL IDEAS """
    # 1. which metro station has the most number of houses nearby
    # 2. which metro station has the most number of amenities
    # 3. which school has the most number of housese nearby
    
    # Getting metro station data
    """ Number of Metros """
    metros = db.map.aggregate([
            {
            "$match": {"railway": "station"}
            }
            # {
            # "$project": {"railway": "$railway",
            #              "name" : "$name",
            #              "type" : "$type"}
            # }
        ])
    print "\nMetros"
    metro_lists = []
    for i in metros:
        print i["name"], "-", i["type"]
        metro_lists.append(i)

    print "\nNumber of Metros:", len(metro_lists)

    # East Falls Church, Vienna/Fairfax-GMU, West Falls Church Metro are nodes
    # And the others are Ways
    # way information doesn't have position data so it has to link to the node information
    # and extract the position data from it.

    print "Find the first node from way information"
    way_nodes = {}
    for i in metro_lists:
        if i["type"] == "way":
            way_nodes[i["name"]] = i["node_refs"][0]
    pprint.pprint(way_nodes)

    nodes_pos = {}
    for node in way_nodes.values():
        db_way_nodes = db.map.aggregate([
                {
                "$match": {"id": node}
                },
                {
                "$project": {"node": "$id",
                             "pos" : "$pos"}
                }
            ])
        for i in db_way_nodes:
            nodes_pos[i["node"]] = i["pos"]
    pprint.pprint(nodes_pos)

    # Find residential type of buildings
    num_metros = db.map.aggregate([
            {
            "$match": {"building": {"$ne": None}}
            },
            {
            "$group": {"_id": "$building", "count": {"$sum": 1}}
            },
            {
            "$sort": {"count": -1}
            }
        ])
    for i in num_metros:
        pprint.pprint(i)

    # list of residential building types
    # "apartments","residential","house", "Townhouse"

    # for each position find the number of houses in a sqaure range +-0.02
    # First gathering building node information
    num_metros = db.map.aggregate([
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
    building_nodes = []
    for i in num_metros:
        building_nodes.append(i["node"][0])

    for node in building_nodes:
        building_nodes_pos = {}
        db_building_nodes_pos = db.map.aggregate([
                {
                "$match": {
                    "type": "node",
                    "id": node,
                    }
                }
            ])
        for i in db_building_nodes_pos:
            building_nodes_pos["node"] = i["id"]
            building_nodes_pos["pos"] = i["pos"]
        db.building.insert(building_nodes_pos)

    print db.building.find_one()
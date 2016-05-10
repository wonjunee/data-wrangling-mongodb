#!/usr/bin/env python
# Run this after "finalProject_dbinsert.py"

import pprint
import codecs
import json

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

    """ Find the street names """
    result = db.map.aggregate([
            {
            "$group" : {
                "_id" : None,
                "streets" : {"$addToSet" : "$address.street"}
                }
            },
            {
            "$sort" : {
                "streets" : 1
                }
            }
        ])
    for i in result:
        street_lists = (i["streets"])
    street_names = {}
    for i in street_lists:
        street_names[i.split(" ")[-1]] = None
    pprint.pprint(street_names)

    result = db.map.aggregate([
            {
            "$group" : {
                "_id" : None,
                "streets" : {"$addToSet" : "$address.postcode"}
                }
            }
        ])
    a = {}
    for i in result:
        pprint.pprint(i["streets"])
    
    result = db.map.aggregate([
            {
            "$group" : {
                "_id" : None,
                "streets" : {"$addToSet" : "$phone"}
                }
            },
            {
            "$sort" : {
                "streets" : 1
                }
            }
        ])
    for i in result:
        pprint.pprint(i)
    
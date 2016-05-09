#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
non_ascii = re.compile(r'[^\x00-\x7f]')
def shape_element(element):
    if element.tag == "node":
        # YOUR CODE HERE
        node = {
            "id": None,
            "visible": None,
            "type": "node",
            "railway": None,
            "amenity": None,
            "name": None,
            "pos": {
                "lat": None,
                "lon": None
                },
            "created" : {
                "changeset": None,
                "user": None,
                "version": None,
                "uid": None,
                "timestamp": None,
                "source" : None
                }
            }
        for line in element.iter(element.tag):
            attr = line.attrib
            # pprint.pprint( attr)
            for key in ["id", "visible"]:
                if key in attr.keys():
                    node[key] = attr[key]
            if "lat" in attr.keys():
                node["pos"]["lat"] = float(attr["lat"])
                node["pos"]["lon"] = float(attr["lon"])
            for key in ["changeset","user","version","uid","timestamp","source"]:
                if key in attr.keys():
                    node["created"][key] = attr[key]
        for i in element.getchildren():
            if "k" in i.attrib.keys():
                if i.attrib["k"] == "source":
                    node["created"]["source"] = non_ascii.sub("",i.attrib["v"])
                elif i.attrib["k"] in ["railway","amenity","name"]:
                    node[i.attrib["k"]] = non_ascii.sub("",i.attrib["v"])
        return node
    elif element.tag == "way":
        a = 0
        way = {
            "id" : None,
            "type": "way",
            "address":{},
            "railway": None,
            "name": None,
            "building" : None,
            "created" : {
                "changeset": None,
                "user": None,
                "version": None,
                "uid": None,
                "timestamp": None,
                "source" : None
            }
        }
        for line in element.iter(element.tag):
            attr = line.attrib
            if "id" in attr.keys():
                way["id"] = attr["id"]
            for key in ["changeset","user","version","uid","timestamp","source"]:
                if key in attr.keys():
                    way["created"][key] = attr[key]
        for i in element.getchildren():
            if "ref" in i.attrib.keys():
                if a == 0:
                    way["node_refs"] = i.attrib["ref"]
                    a = 1
                else:
                    pass
            elif "k" in i.attrib.keys():
                if len(i.attrib["k"].split(":")) == 2:
                    if i.attrib["k"].split(":")[1] in ["housenumber", "street"]:
                        way["address"][i.attrib["k"].split(":")[1]] = i.attrib["v"]
                elif i.attrib["k"] == "source":
                    way["created"]["source"] = non_ascii.sub("",i.attrib["v"])
                elif i.attrib["k"] in ["building", "railway", "name"]:
                    way[i.attrib["k"]] = non_ascii.sub("",i.attrib["v"])
        return way
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('c:/map', False)

    # print
    # for i in data:
    #     pprint.pprint(i)
    # print

    correct_first_elem = {
        "id": "246574", 
        "visible": None, 
        "type": "node", 
        "railway": None,
        "amenity": None,
        "name": None,
        "pos": {
            "lat": 38.8695350,
            "lon": -77.1495846
        },
        "created": {
            "changeset": "19557774", 
            "user": "Jason Gottshall", 
            "version": "3", 
            "uid": "1677159", 
            "timestamp": "2013-12-20T22:10:17Z",
            "source":None
        }
    }

    correct_last_elem = {
        "id" : "51055714",
        "type" : "way",
        "node_refs" : ["586966672", "586966674", "1705359501", "586966677"],
        "address":{},
        "created" : {
            "changeset": "17187004",
            "user": "Your Village Maps",
            "version": "9",
            "uid": "227972",
            "timestamp": "2013-08-02T03:05:08Z",
            "source" : None
        }  
    }

    assert data[0] == correct_first_elem
    # assert data[-1] == correct_last_elem
    print "Good!"
if __name__ == "__main__":
    test()
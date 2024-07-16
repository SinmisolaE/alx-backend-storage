#!/usr/bin/env python3

""" function that inserts a new document in a collection based on kwargs"""

import pymongo


def insert_school(mongo_collection, **kwargs):
    """ Returns the new _id """

    new = mongo_collection.insert_one(kwargs)
    return new.inserted_id

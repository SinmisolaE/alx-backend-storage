#!/usr/bin/env python3

""" function that lists all documents in a collection """


import pymongo


def list_all(mongo_collection):
    """ Return an empty list if no document in the collection
        else return the list of documents
    """

    if not mongo_collection:
        return []

    documents = mongo_collection.find()
    return [doc for doc in documents]

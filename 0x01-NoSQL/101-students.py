#!/usr/bin/env python3

""" function that returns all students sorted by average score """

import pymongo


def top_students(mongo_collection):
    """ The top must be ordered
        The average score must be part of each item
        returns with key = averageScore
    """

    return mongo_collection.aggregate([
        {
            "$project":
                {"name": "$name",
                 "averageScore": {"$avg": "$topics.score"}}
        },
        {
            "$sort":
                {
                    "averageScore": -1
                }
        }
        ])

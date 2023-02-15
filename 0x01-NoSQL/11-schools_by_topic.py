#!/usr/bin/env python3
""" function that returns the list of school having a specific topic """


def schools_by_topic(mongo_collection, topic):
    """
    returns the list of school having a specific topic

    Argument:
    mongo_collection: pymongo object
    topic: string - the topics to be searched
    """
    return mongo_collection.find({"topics": {"$in": [topic]}})

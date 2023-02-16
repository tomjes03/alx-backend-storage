#!/usr/bin/env python3
""" function that changes all topics of a school document based on the name """


def update_topics(mongo_collection, name, topics):
    """
    changes all topics of a school document based on the name

    Argument:
    mongo_collection: pymongo object
    name: string - the school name to update
    topics: list of strings - the list of topics approached in the school
    """
    mongo_collection.update_many({'name': name}, {'$set': {'topics': topics}})

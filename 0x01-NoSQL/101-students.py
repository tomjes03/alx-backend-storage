#!/usr/bin/env python3
""" function that returns all students sorted by average score """


def top_students(mongo_collection):
    """
    returns the list of school having a specific topic

    Argument:
    mongo_collection: pymongo object
    """
    all_students = mongo_collection.aggregate(
        [
            {"$match": {}},
            {"$unwind": "$topics"},
            {"$group": {"_id": "$name", "averageScore": {"$avg": "$topics.score"}}},
            {"$sort": {"averageScore": -1}},
        ]
    )
    for student in all_students:
        mongo_collection.update_one(
            {"name": student.get("_id")},
            {"$set": {"averageScore": student.get("averageScore")}}
        )
    all_students = mongo_collection.find().sort("averageScore", -1)
    return all_students

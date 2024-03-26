#!/usr/bin/env python3
"""
Function to retrieve top students based on average score
"""

def top_students(mongo_collection):
    """
    Retrieves all students sorted by their average score
    :param mongo_collection: MongoDB collection containing student data
    :return: Cursor with students sorted by average score in descending order
    """
    return mongo_collection.aggregate([
        {"$project": {
            "name": "$name",
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ])

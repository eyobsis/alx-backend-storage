#!/usr/bin/env python3

"""
Module: 11-schools_by_topic
This module contains a function to retrieve a list of schools
based on a specific topic from a MongoDB collection.
"""


def schools_by_topic(mongo_collection, topic):
    """
    Retrieve a list of schools that cover a specific topic from
    a MongoDB collection.

    Args:
    - mongo_collection: pymongo collection object
    - topic (string): topic to search for in schools

    Returns:
    - List of schools matching the specified topic
    """
    schools = mongo_collection.find({'topics': topic})
    return list(schools)


if __name__ == "__main__":
    pass

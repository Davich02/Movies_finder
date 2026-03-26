import pymongo

from log_writer import collection


def get_top_searches():
    result = collection.aggregate([{
        "$group": {
            "_id": "$search_type",
            "count": {"$sum": 1},
        }},
        {"%sort": {"count": 1}},
        {"$limit":5}
    ])
    return list(result)


def get_recent_searches():
    result = collection.find().sort("timestamp", -1).limit(5)
    return list(result)
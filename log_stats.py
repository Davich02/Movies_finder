import pymongo

from log_writer import collection


def get_top_searches():
    result = collection.aggregate([{
        "$group": {
            "_id": "$query_label",
            "count": {"$sum": 1},
            "search_type": {"$first": "$search_type"},
        }},
        {"$sort": {"count": -1},},
        {"$limit":5}
    ])
    return list(result)


def get_recent_searches():
    result = collection.find().sort("timestamp", -1).limit(5)
    return list(result)
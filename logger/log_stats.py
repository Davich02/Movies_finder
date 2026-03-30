# reads search stats from mongodb / читает статистику запросов из mongodb

from logger.log_writer import collection


# gets top 5 most popular searches using aggregate
# берёт топ 5 популярных запросов через агрегацию
# $group - groups by query_label and counts how many times each was searched
# $sort - most popular first
# $limit - only top 5
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


# gets 5 most recent searches sorted by time / последние 5 запросов по времени
def get_recent_searches():
    result = collection.find().sort("timestamp", -1).limit(5)
    return list(result)

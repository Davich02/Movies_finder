"""Analytics module. Reads search history from MongoDB for statistics.
Модуль аналитики. Читает историю поиска из MongoDB для статистики.
"""

from logger.log_writer import collection


def get_top_searches():
    """Return top 5 most frequent search queries using MongoDB aggregation pipeline.
    Возвращает топ 5 популярных запросов через агрегацию MongoDB.

    Pipeline:
        $group  - groups documents by query_label, counts occurrences
        $sort   - sorts by count descending (most popular first)
        $limit  - takes only top 5
    """
    result = collection.aggregate([{
        "$group": {
            "_id": "$query_label",
            "count": {"$sum": 1},
            "search_type": {"$first": "$search_type"},
        }},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ])
    return list(result)


def get_recent_searches():
    """Return 5 most recent unique searches grouped by query_label with count.
    Возвращает 5 последних уникальных запросов со счётчиком.

    Pipeline:
        $group  - groups by query_label, counts occurrences, keeps last timestamp
        $sort   - sorts by last_time descending (most recent first)
        $limit  - takes only 5
    """
    result = collection.aggregate([{
        "$group": {
            "_id": "$query_label",
            "count": {"$sum": 1},
            "search_type": {"$first": "$search_type"},
            "params": {"$first": "$params"},
            "last_time": {"$max": "$timestamp"},
        }},
        {"$sort": {"last_time": -1}},
        {"$limit": 5}
    ])
    return list(result)

#!/usr/bin/env python3
"""
Aggregation
"""

from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    print(f'{logs_collection.count_documents(filter={})} logs')
    print('Methods:')
    print(f'\tmethod GET: {logs_collection.count_documents( filter={"method": "GET"} )}')
    print(f'\tmethod POST: {logs_collection.count_documents( filter={"method": "POST"} )}')
    print(f'\tmethod PUT: {logs_collection.count_documents( filter={"method": "PUT"} )}')
    print(f'\tmethod PATCH: {logs_collection.count_documents( filter={"method": "PATCH"} )}')
    print(f'\tmethod DELETE: {logs_collection.count_documents( filter={"method": "DELETE"} )}')
    print(f'{logs_collection.count_documents( filter={"method": "GET", "path": "/status"} )} status check')
    print(f'IPs:')
    ip_count = logs_collection.aggregate(
        [
            {"$match": {}},
            {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
    )
    for ip in ip_count:
        print(f'\t{ip.get("_id")}: {ip.get("count")}')

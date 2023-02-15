#!/usr/bin/env python3
"""
Module to give stats on nginx logs
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

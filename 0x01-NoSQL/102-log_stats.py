#!/usr/bin/env python3
"""
Script to display statistics and top 10 IPs from Nginx logs stored in MongoDB
"""
from pymongo import MongoClient

def log_stats():
    """
    Display statistics and top 10 IPs from Nginx logs
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    total_logs = logs_collection.count_documents({})
    get_count = logs_collection.count_documents({"method": "GET"})
    post_count = logs_collection.count_documents({"method": "POST"})
    put_count = logs_collection.count_documents({"method": "PUT"})
    patch_count = logs_collection.count_documents({"method": "PATCH"})
    delete_count = logs_collection.count_documents({"method": "DELETE"})
    status_check_count = logs_collection.count_documents({"method": "GET", "path": "/status"})

    print(f"{total_logs} logs")
    print("Methods:")
    print(f"\tmethod GET: {get_count}")
    print(f"\tmethod POST: {post_count}")
    print(f"\tmethod PUT: {put_count}")
    print(f"\tmethod PATCH: {patch_count}")
    print(f"\tmethod DELETE: {delete_count}")
    print(f"{status_check_count} status check")
    print("IPs:")

    sorted_ips = logs_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    for ip_data in sorted_ips:
        print(f"\t{ip_data.get('_id')}: {ip_data.get('count')}")

if __name__ == "__main__":
    log_stats()

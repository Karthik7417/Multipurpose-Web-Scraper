from bson import ObjectId
from datetime import datetime
from pymongo import MongoClient, ASCENDING
import queue_jobs
from settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE, CRAWL_DEPTH


def create_task(task):
    task["created_on"] = datetime.utcnow()
    with MongoClient(MONGODB_HOST, MONGODB_PORT) as conn:
        return conn[MONGODB_DATABASE]["tasks"].insert_one(task).inserted_id


def delete_task(task_id):
    with MongoClient(MONGODB_HOST, MONGODB_PORT) as conn:
        conn[MONGODB_DATABASE]["tasks"].delete_one({"_id": ObjectId(task_id)})
        conn[MONGODB_DATABASE].drop_collection("{}_websites".format(task_id))
        conn[MONGODB_DATABASE].drop_collection("{}_validated".format(task_id))
        conn[MONGODB_DATABASE].drop_collection("{}_pages".format(task_id))
        conn[MONGODB_DATABASE].drop_collection("{}_entities".format(task_id))


def get_all_tasks():
    with MongoClient(MONGODB_HOST, MONGODB_PORT) as conn:
        tasks = conn[MONGODB_DATABASE]["tasks"].find()
    return list(tasks)


def get_task(task_id):
    with MongoClient(MONGODB_HOST, MONGODB_PORT) as conn:
        task = conn[MONGODB_DATABASE]["tasks"].find_one({"_id": ObjectId(task_id)})
        task["websites_count"] = conn[MONGODB_DATABASE]["{}_websites".format(task_id)].count()
        task["validated_count"] = conn[MONGODB_DATABASE]["{}_validated".format(task_id)].count()
        task["pages_count"] = conn[MONGODB_DATABASE]["{}_pages".format(task_id)].count()
        task["entities_count"] = conn[MONGODB_DATABASE]["{}_entities".format(task_id)].count()
        websites_sts = conn[MONGODB_DATABASE]["{}_websites".format(task_id)].aggregate(
            [{"$group": {"_id": "$status", "count": {"$sum": 1}}},
             {"$sort": {"_id": 1}}])
        task["websites_sts"] = ", ".join(["{} {}".format(x["count"], x["_id"]) for x in websites_sts])
    return task


def get_input_websites(task_id):
    with MongoClient(MONGODB_HOST, MONGODB_PORT) as conn:
        websites = conn[MONGODB_DATABASE]["{}_websites".format(task_id)].find().sort([("website_name", ASCENDING),
                                                                                      ("website_url", ASCENDING)])
    return websites


def get_validated_websites(task_id):
    with MongoClient(MONGODB_HOST, MONGODB_PORT) as conn:
        websites = conn[MONGODB_DATABASE]["{}_validated".format(task_id)].aggregate([
            {
                "$lookup":
                    {
                        "from": "{}_websites".format(task_id),
                        "localField": "_id",
                        "foreignField": "_id",
                        "as": "input"
                    }
            },
            {
                "$project":
                    {
                        "website_url": 1,
                        "input": {"$arrayElemAt": ["$input", 0]}
                    }
            },
            {
                "$project":
                    {
                        "website_url": 1,
                        "website_name": "$input.website_name",
                        "original_url": "$input.website_url",
                        "keywords": "$input.keywords"
                    }
            },
            {
                "$sort": {"website_name": 1, "website_url": 1}
            }
        ])
    return websites


def get_crawled_pages(task_id):
    with MongoClient(MONGODB_HOST, MONGODB_PORT) as conn:
        websites = conn[MONGODB_DATABASE]["{}_pages".format(task_id)].aggregate([
            {
                "$group": {
                    "_id": {"$toObjectId": "$website_id"},
                    "count": {"$sum": 1}
                }
            },
            {
                "$lookup":
                    {
                        "from": "{}_websites".format(task_id),
                        "localField": "_id",
                        "foreignField": "_id",
                        "as": "input"
                    }
            },
            {
                "$lookup":
                    {
                        "from": "{}_validated".format(task_id),
                        "localField": "_id",
                        "foreignField": "_id",
                        "as": "url"
                    }
            },
            {
                "$project":
                    {
                        "count": 1,
                        "input": {"$arrayElemAt": ["$input", 0]},
                        "url": {"$arrayElemAt": ["$url", 0]}
                    }
            },
            {
                "$project":
                    {
                        "count": 1,
                        "website_name": "$input.website_name",
                        "website_url": "$url.website_url"
                    }
            },
            {
                "$sort": {"website_name": 1, "website_url": 1}
            }
        ])
    return websites


def get_parsed_entities(task_id):
    with MongoClient(MONGODB_HOST, MONGODB_PORT) as conn:
        websites = conn[MONGODB_DATABASE]["{}_entities".format(task_id)].aggregate([
            {
                "$group": {
                    "_id": "$website_id",
                    "count": {"$sum": 1}
                }
            },
            {
                "$lookup":
                    {
                        "from": "{}_websites".format(task_id),
                        "localField": "_id",
                        "foreignField": "_id",
                        "as": "input"
                    }
            },
            {
                "$lookup":
                    {
                        "from": "{}_validated".format(task_id),
                        "localField": "_id",
                        "foreignField": "_id",
                        "as": "url"
                    }
            },
            {
                "$project":
                    {
                        "count": 1,
                        "input": {"$arrayElemAt": ["$input", 0]},
                        "url": {"$arrayElemAt": ["$url", 0]}
                    }
            },
            {
                "$project":
                    {
                        "count": 1,
                        "website_name": "$input.website_name",
                        "website_url": "$url.website_url"
                    }
            },
            {
                "$sort": {"website_name": 1, "website_url": 1}
            }
        ])
    return websites


def insert_task_websites(task_id, documents):
    with MongoClient(MONGODB_HOST, MONGODB_PORT) as conn:
        conn[MONGODB_DATABASE]["{}_websites".format(task_id)].insert(documents)


def update_task(task):
    with MongoClient(MONGODB_HOST, MONGODB_PORT) as conn:
        task_id = task.pop("_id", None)
        conn[MONGODB_DATABASE]["tasks"].update_one({"_id": ObjectId(task_id)}, {"$set": task})
        return task_id


def validate_websites(task_id):
    with MongoClient(MONGODB_HOST, MONGODB_PORT) as conn:
        for website in conn[MONGODB_DATABASE]["{}_websites".format(task_id)].find():
            queue_jobs.validate_url(task_id, str(website["_id"]), website["website_url"], website["keywords"])
            conn[MONGODB_DATABASE]["{}_websites".format(task_id)].update_one({"_id": website["_id"]},
                                                                             {"$set": {"status": "sent"}})


def crawl_websites(task_id):
    with MongoClient(MONGODB_HOST, MONGODB_PORT) as conn:
        for website in conn[MONGODB_DATABASE]["{}_validated".format(task_id)].find():
            queue_jobs.crawl_website(task_id, str(website["_id"]), website["website_url"], CRAWL_DEPTH)


def parse_pages(task_id):
    with MongoClient(MONGODB_HOST, MONGODB_PORT) as conn:
        for page in conn[MONGODB_DATABASE]["{}_pages".format(task_id)].find():
            queue_jobs.parse_page(task_id, str(page["_id"]))

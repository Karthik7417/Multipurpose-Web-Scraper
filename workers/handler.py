try:
    import unzip_requirements
except ImportError:
    pass
from settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME, DEBUG_QUEUE_URL
import sys
import importlib
spec = importlib.util.spec_from_file_location("_sqlite3", "./dummysqllite.py")
sys.modules["_sqlite3"] = importlib.util.module_from_spec(spec)
sys.modules["sqlite3"] = importlib.util.module_from_spec(spec)
sys.modules["sqlite3.dbapi2"] = importlib.util.module_from_spec(spec)
import nltk

import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

nltk.data.path.append(os.getenv('NLTK_DATA'))

import json
from pythonScripts.validate import process_validate_url
from pythonScripts.crawl import crawl
from pythonScripts.parser import extract_all

# debug_sqs = boto3.client("sqs", aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
#                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
#                    region_name=os.getenv('REGION_NAME'))


def action_switch(event, context):
    for record in event['Records']:
        print("record :", record)
        payload = json.loads(record["body"])

        if payload["action"] == "VALIDATE":
            task_id = payload["task_id"]
            website_id = payload["website_id"]
            website_url = payload["website_url"]
            keywords = payload["keywords"]

            process_validate_url(task_id, website_id, website_url, keywords)

        elif payload["action"] == "CRAWL":
            task_id = payload["task_id"]
            website_id = payload["website_id"]
            website_url = payload["website_url"]
            depth = payload["depth"]
            crawl(task_id, website_id, website_url, depth)

        elif payload["action"] == "PARSE":
            task_id = payload["task_id"]
            page_id = payload["page_id"]
            extract_all(task_id, page_id)

        else:
            print("Invalid Action")
    return ' '

def queue_listener():
    pass

if __name__ == "__main__":
    queue_listener()

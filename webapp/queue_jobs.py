import boto3
import json
from settings import AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, REGION_NAME, QUEUE_URL

# sqs = boto3.client("sqs", aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID') , aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'), region_name=os.getenv('REGION_NAME'))

sqs = boto3.client("sqs", aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION_NAME)


def validate_url(task_id, website_id, website_url, keywords):
    action = "VALIDATE"
    message = json.dumps({"action": action,
                          "task_id": task_id,
                          "website_id": website_id,
                          "website_url": website_url,
                          "keywords": keywords})
    sqs.send_message(QueueUrl=QUEUE_URL,
                     MessageBody=message,
                     MessageAttributes={
                         "Action": {
                             "DataType": "String",
                             "StringValue": action
                         }
                     })


def crawl_website(task_id, website_id, website_url, crawl_depth):
    action = "CRAWL"
    message = json.dumps({"action": action,
                          "task_id": task_id,
                          "website_id": website_id,
                          "depth": crawl_depth,
                          "website_url": website_url
                          })

    sqs.send_message(QueueUrl=QUEUE_URL,
                     MessageBody=message,
                     MessageAttributes={
                         "Action": {
                             "DataType": "String",
                             "StringValue": action
                         }
                     })


def parse_page(task_id, page_id):
    action = "PARSE"
    message = json.dumps({"action": action,
                          "task_id": task_id,
                          "page_id": page_id})
    sqs.send_message(QueueUrl=QUEUE_URL,
                     MessageBody=message,
                     MessageAttributes={
                         "Action": {
                             "DataType": "String",
                             "StringValue": action
                         }
                     })

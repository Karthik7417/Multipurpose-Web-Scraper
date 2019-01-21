import boto3
import json

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='WebScraperSQS')

def crawl_website(task_id, website_id, website_url, crawl_depth):
    action = "CRAWL"
    message = json.dumps({"action": action,
                          "task_id": task_id,
                          "website_id": website_id,
                          "depth": crawl_depth,
                          "website_url": website_url
                          })

    queue.send_message(
                     MessageBody=message,
                     MessageAttributes={
                         "Action": {
                             "DataType": "String",
                             "StringValue": action
                         }
                     })

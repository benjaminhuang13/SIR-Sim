import boto3
import os
import json

def sendSuccessResults(region, results):
   sqs = boto3.client('sqs', region_name=region)
   queue = os.environ["RESULTS_SUCCESS_QUEUE"]
   json_results = json.dumps(results)
   sqs.send_message(QueueUrl=queue, MessageBody=json_results)

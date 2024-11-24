import boto3
import os
import json

class sqsHandler:

   def __init__(self, region):
      self.sqs = boto3.client('sqs', region_name=region)
      self.queue = os.environ["RESULTS_SUCCESS_QUEUE"]

   def sendSuccessResults(self, results):
      json_results = json.dumps(results)
      self.sqs.send_message(QueueUrl=self.queue, MessageBody=json_results)
      
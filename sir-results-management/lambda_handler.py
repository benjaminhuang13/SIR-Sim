import os
import json
import sqs_handler
import time_stream_interface
import logging

def lambda_handler(event, context):

   logging.basicConfig(level=logging.INFO) 
   logger = logging.getLogger()

   region = os.environ["AWS_REGION"]

   # TODO - I don't believe we are doing batch lambdas for this.
   #  May need to add a loop through the records
   results_json =  event['Records'][0]['body']
   results = json.loads(results_json)

   success, errMessage = time_stream_interface.writeResults(region, results)

   if success:
      # If successful send event to successful write queue
      sqs_handler.sendSuccessResults(region, results_json)

      return {
         'statusCode': 200,
         'body': 'Results successfully written'
      }
   else:
      logger.error("Failed to write to Timestream: " + errMessage)
      return {
         'statusCode': 500,
         'body': errMessage
      }
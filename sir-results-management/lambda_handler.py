import os
import json
import sqs_handler
import time_stream_interface


def lambda_handler(event, context):
   region = os.environ["AWS_REGION"]

   print("Handling Lambda Event: " + str(event))

   # TODO - I don't believe we are doing batch lambdas for this.
   #  May need to add a loop through the records
   results_json =  event['Records'][0]['body']
   results = json.loads(results_json)

   timeStream = time_stream_interface.timeStreamHandler(region)
   success, errMessage = timeStream.writeResults(results)

   if success:
      # If successful send event to successful write queue
      sqs = sqs_handler.sqsHandler(region)
      sqs.sendSuccessResults(results_json)

      return {
         'statusCode': 200,
         'body': 'Results successfully written'
      }
   else:
      return {
         'statusCode': 500,
         'body': errMessage
      }
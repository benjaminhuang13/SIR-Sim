import json
import os
import time_stream_interface
import messages_pb2
from google.protobuf import json_format


def lambda_handler(event, context):
   
   sim_results = messages_pb2.SimResults()
   data = json_format(event, sim_results)

   timeStream = time_stream_interface.timeStreamHandler(os.environ["REGION"])
   timeStream.writeResults(data)

   # TODO - Get results from write records
   return {
        'statusCode': 200,
        'body': 'Results successfully written'
    }
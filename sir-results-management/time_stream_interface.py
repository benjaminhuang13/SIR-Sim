import sys
import os
import boto3
from botocore.config import Config
from datetime import datetime, timezone

class timeStreamHandler:

   def __init__(self, region):
      self.write_client = boto3.Session().client('timestream-write', config=Config(read_timeout=20, max_pool_connections = 5000, retries={'max_attempts': 10}))
      self.dimensions = [ {'Name': 'region', 'Value': region} ]

   def writeResults(self, simResults):

      writeRecords = []

      for result in simResults:

         print(result)

         # Convert date time to milliseconds epoch as a string
         time = str(round(result['time'].timestamp() * 1000))

         num_infected = {
            'Dimensions': self.dimensions,
            'MeasureName': 'num_infected',
            'MeasureValue': str(result['numInfected']),
            'MeasureValueType': 'BIGINT',
            'Time': time
         }

         num_susceptible = {
            'Dimensions': self.dimensions,
            'MeasureName': 'num_susceptible',
            'MeasureValue': str(result['numSusceptible']),
            'MeasureValueType': 'BIGINT',
            'Time': time
         }

         num_recovered = {
            'Dimensions': self.dimensions,
            'MeasureName': 'num_recovered',
            'MeasureValue': str(result['numRecovered']),
            'MeasureValueType': 'BIGINT',
            'Time': time
         }
         
         writeRecords.extend([num_infected, num_susceptible, num_recovered])

      success = False
      try:
         result = self.write_client.write_records(DatabaseName=os.environ["DATABASE_NAME"], TableName=os.environ["TABLE_NAME"],
                  Records=writeRecords, CommonAttributes={})
         print("WriteRecords Status: [%s]" % result['ResponseMetadata']['HTTPStatusCode'])
         success = True
      except self.client.exceptions.RejectedRecordsException as err:
         self._print_rejected_records_exceptions(err)
      except Exception as err:
         print("Error:", err)

      return success

   

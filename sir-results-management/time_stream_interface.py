import os
import boto3
from botocore.config import Config
from datetime import datetime

# sources: 
#  https://github.com/awslabs/amazon-timestream-tools/blob/mainline/sample_apps/python/SampleApplication.py
#  https://docs.aws.amazon.com/timestream/latest/developerguide/code-samples.run-query.html

def writeResults(region, simResults):

   write_client = boto3.Session().client('timestream-write', 
                                                config=Config(region_name = region, read_timeout =20, 
                                                            max_pool_connections = 5000, retries={'max_attempts': 10}))
   dimensions = [ {'Name': 'region', 'Value': region} ]
   database_name = DatabaseName=os.environ["DATABASE_NAME"]
   table_name = DatabaseName=os.environ["TABLE_NAME"]

   writeRecords = []
   for result in simResults['results']:

      # Convert date time to milliseconds epoch as a string
      time = str(datetime.now().timestamp() * 1000)

      sim_time = {
         'Dimensions': dimensions,
         'MeasureName': 'sim_time',
         'MeasureValue': str(result['time']),
         'MeasureValueType': 'BIGINT',
         'Time': time
      }

      num_infected = {
         'Dimensions': dimensions,
         'MeasureName': 'num_infected',
         'MeasureValue': str(result['numInfected']),
         'MeasureValueType': 'BIGINT',
         'Time': time
      }

      num_infected = {
         'Dimensions': dimensions,
         'MeasureName': 'num_infected',
         'MeasureValue': str(result['numInfected']),
         'MeasureValueType': 'BIGINT',
         'Time': time
      }

      num_susceptible = {
         'Dimensions': dimensions,
         'MeasureName': 'num_susceptible',
         'MeasureValue': str(result['numSusceptible']),
         'MeasureValueType': 'BIGINT',
         'Time': time
      }

      num_recovered = {
         'Dimensions': dimensions,
         'MeasureName': 'num_recovered',
         'MeasureValue': str(result['numRecovered']),
         'MeasureValueType': 'BIGINT',
         'Time': time
      }
      
      writeRecords.extend([sim_time, num_infected, num_susceptible, num_recovered])

   success = False
   message = ""
   try:
      result = write_client.write_records(DatabaseName=os.environ["DATABASE_NAME"], TableName=os.environ["TABLE_NAME"],
               Records=writeRecords, CommonAttributes={})
      #print("WriteRecords Status: [%s]" % result['ResponseMetadata']['HTTPStatusCode'])
      success = result['ResponseMetadata']['HTTPStatusCode'] == 200
      message = "Success"
   except write_client.exceptions.RejectedRecordsException as err:
      _print_rejected_records_exceptions(err)
      message = "Failed to write records to time stream database."
   except Exception as err:
      print("Error:", err)
      message = "Unknown error. See logger for more details."

   return success, message

# Source: https://github.com/awslabs/amazon-timestream-tools/blob/mainline/sample_apps/python/QueryExample.py
# Start and End time are milliseconds epoch
def readResults(region, startTime, endTime):
   query_client = boto3.Session().client('timestream-query', config=Config(region_name = region))
   database_name = DatabaseName=os.environ["DATABASE_NAME"]
   table_name = DatabaseName=os.environ["TABLE_NAME"]

   query = \
      "WITH Results AS ( " \
      "SELECT time, measure_name, measure_value::bigint as value " \
      "FROM \"" + database_name + "\".\""+ table_name + "\") " \
      "SELECT infected.time, infected.value AS numInfected, susceptible.value AS numSusceptible, recovered.value AS numRecovered " \
      "FROM Results infected " \
      "LEFT JOIN Results susceptible ON infected.time = susceptible.time AND susceptible.measure_name = 'num_susceptible' " \
      "LEFT JOIN Results recovered ON infected.time = recovered.time AND recovered.measure_name = 'num_recovered' " \
      "WHERE infected.measure_name = 'num_infected' " \
      "AND infected.time between from_milliseconds(" + str(round(startTime)) + ") and from_milliseconds(" + str(round(endTime)) + ")" \
      "ORDER BY infected.time DESC"
   
   read_data = []

   try:
      iterator = query_client.get_paginator('query').paginate(QueryString=query)
      for page in iterator:
         column_info = page['ColumnInfo']
         for row in page['Rows']:
            data = _parse_row(column_info, row)
            read_data.append(data)   
   except Exception as err:
      print("Failed to query database", err)
   
   results = { 
      'results' : read_data 
   }

   return results

# Following is a generic parsing from https://docs.aws.amazon.com/timestream/latest/developerguide/code-samples.run-query.html
def _parse_row(self, column_info, row):
   data = row['Data']
   row_output = {}
   for j in range(len(data)):
      info = column_info[j]
      datum = data[j]   
      key, value = self._parse_datum(info, datum)
      row_output[key] = value

   return row_output

def _parse_datum(self, info, datum):
   if datum.get('NullValue', False):
      print("Error - null value was queried")
      return "", 0

   column_type = info['Type']

   # If the column is of Scalar Type
   if 'ScalarType' in column_type:
      return self._parse_column_name(info), self._convert_value(info, datum['ScalarValue'])
   else:
      print("Error - Invalid input type queried")
      return "", 0

def _parse_column_name(self, info):
   if 'Name' in info:
      return info['Name']
   else:
      print("Error - Queried column has no name")
      return ""
   
def _convert_value(self, info, str_value):
   column_type = info['Type']
   #print("Converting value type " + column_type + ", value: " + str_value)
   if 'ScalarType' in column_type:
      format = column_type['ScalarType']
      if(format == 'TIMESTAMP'):
         format_str = '%Y-%m-%d %H:%M:%S.%f'
         # Remove nano-second portion of string
         time_str = str_value[:-3]
         datetime_obj = datetime.strptime(time_str, format_str)
         # return epoch milliseconds
         return int(datetime_obj.timestamp() * 1000)
      elif(format == 'BIGINT'):
         return int(str_value)
      else:
         # Not supported type
         return str_value
   else:
      # Non-scalar values not supported at this time
      return str_value
   
def _print_rejected_records_exceptions(err):
   print("RejectedRecords: ", err)
   for rr in err.response["RejectedRecords"]:
      print("Rejected Index " + str(rr["RecordIndex"]) + ": " + rr["Reason"])
      if "ExistingVersion" in rr:
         print("Rejected record existing version: ", rr["ExistingVersion"])
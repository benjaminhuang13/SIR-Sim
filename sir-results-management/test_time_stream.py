import os
import unittest
import time_stream_interface
from datetime import datetime

# Note that tests will fail if AWS credentials is not setup.
class TestTimeStream(unittest.TestCase):

   def test_read_after_write(self):
      # Setup environment variables
      os.environ['DATABASE_NAME'] = 'sir-sim-results'
      os.environ['TABLE_NAME'] = 'results'

      timeStream = time_stream_interface.timeStreamHandler('us-east-1')
      start_time = datetime.now().timestamp()  * 1000

      result = {
         'time': int(datetime.now().timestamp() * 1000),
         'numSusceptible': 1,
         'numInfected': 2,
         'numRecovered': 3,
      }

      dailyResults = { 
         'results' : [result]
      }

      success = timeStream.writeResults(dailyResults)
      self.assertTrue(success)

      read_results = timeStream.readResults(start_time - 1000, datetime.now().timestamp()  * 1000)
      self.assertEqual(1, read_results['results'][0]['numSusceptible'])
      self.assertEqual(2, read_results['results'][0]['numInfected'])
      self.assertEqual(3, read_results['results'][0]['numRecovered'])


if __name__ == '__main__':
   unittest.main()

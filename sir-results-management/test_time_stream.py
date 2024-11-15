import os
import unittest
import time_stream_interface
from datetime import datetime

class TestTimeStream(unittest.TestCase):

   def test_write(self):
      # Setup environment variables
      os.environ['DATABASE_NAME'] = 'sir-sim-results'
      os.environ['TABLE_NAME'] = 'results'

      timeStream = time_stream_interface.timeStreamHandler('us-east-1')

      result = {
         'time': datetime.now(),
         'numSusceptible': 1,
         'numInfected': 2,
         'numRecovered': 3,
      }

      dailyResults = [result]

      timeStream.writeResults(dailyResults)


if __name__ == '__main__':
   unittest.main()
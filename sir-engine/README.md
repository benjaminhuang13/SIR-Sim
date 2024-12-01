## Create SQS Queues:

- Input queue for receiving simulation requests
- Output queue for simulation results
- Set environment variable (in lambda_handler.py for now) for OUTPUT_QUEUE_URL

Create ECR and Lambda Function:

1. Create ECR and click the "View Push Commands"
2. Build the sir-engine Dockerfile, tag, push it to new ECR
3. Create lambda from the ECR image. NOTE: Docker buildx >= 0.1.0 makes a manifest (several images). Pick the one that works :-)
4. Set lambda execution role with `AmazonSQSFullAccess` permissions
5. Configure SQS input queue as trigger

## Test:

Test Lambda -> SQS pipeline by giving the input SQS the following json (simulated output from frontend):

```
{'version': '2.0', 'routeKey': 'PUT /sirsim/data', 'rawPath': '/prd/sirsim/data', 'rawQueryString': '', 'headers': {'accept': 'application/json, text/plain, */*', 'accept-encoding': 'gzip, deflate, br, zstd', 'accept-language': 'en-US,en;q=0.5', 'content-length': '120', 'content-type': 'application/json', 'host': 'gp8rnrotf4.execute-api.us-east-1.amazonaws.com', 'origin': 'http://sir-sim.com.s3-website-us-east-1.amazonaws.com', 'priority': 'u=0', 'referer': 'http://sir-sim.com.s3-website-us-east-1.amazonaws.com/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0', 'x-amzn-trace-id': 'Root=1-674cde61-30ae29344c88bed12a3426bd', 'x-forwarded-for': '108.21.59.23', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'requestContext': {'accountId': '471112517107', 'apiId': 'gp8rnrotf4', 'domainName': 'gp8rnrotf4.execute-api.us-east-1.amazonaws.com', 'domainPrefix': 'gp8rnrotf4', 'http': {'method': 'PUT', 'path': '/prd/sirsim/data', 'protocol': 'HTTP/1.1', 'sourceIp': '108.21.59.23', 'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0'}, 'requestId': 'CIevWjqaIAMEZRQ=', 'routeKey': 'PUT /sirsim/data', 'stage': 'prd', 'time': '01/Dec/2024:22:08:33 +0000', 'timeEpoch': 1733090913826}, 'body': '{"userInputs":{"populationSize":"1000","infectionRate":"2","numInfected":"100","recoveryRate":"5","timeStepsDays":"10"}}', 'isBase64Encoded': False}
```

Output:

```
[{'results': [{'time': 1733088168, 'numSusceptible': 988, 'numInfected': 11, 'numRecovered': 1}, {'time': 1733174568, 'numSusceptible': 985, 'numInfected': 13, 'numRecovered': 2}, {'time': 1733260968, 'numSusceptible': 982, 'numInfected': 15, 'numRecovered': 3}]}]
```

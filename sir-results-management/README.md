# SIR SIM Results Manager

## Create ECR and Lambda Function:

Prereq: Install Docker

1. Create ECR and click the "View Push Commands"
2. Build the sir-engine Dockerfile, tag, push it to new ECR
3. Create lambda from the ECR image. NOTE: Docker buildx >= 0.1.0 makes a manifest (several images). Pick the one that works :-)
4. Set lambda execution role with `AmazonSQSFullAccess` permissions
5. Configure `engine-results` SQS input queue as trigger
6. Configure Environmental Variables:

- `DATABASE_NAME` `sir-sim`
- `RESULTS_SUCCESS_QUEUE` `https://sqs.us-east-1.amazonaws.com/457062846495/results-success`
- `TABLE_NAME` `results`

## Environment Variables Required

- AWS_ACCESS_KEY
- AWS_SECRET_ACCESS_KEY
- DATABASE_NAME
- TABLE_NAME
- RESULTS_SUCCESS_QUEUE

## Create Timestream Database

There was a job added in automation to create database if it does not exist.
However, if needed to create one manually, either the AWS console will work or run CLI commands:

`aws timestream-write create-database --database-name sir-sim`
Output:

```
{
    "Database": {
        "Arn": "arn:aws:timestream:us-east-1:[ACCOUNT_ID]:database/sir-sim",
        "DatabaseName": "sir-sim",
        "TableCount": 0,
        "KmsKeyId": "arn:aws:kms:us-east-1:[ACCOUNT_ID]:key/9081505d-9351-4592-8b64-09870978",
        "CreationTime": "2024-12-03T17:39:47.072000-05:00",
        "LastUpdatedTime": "2024-12-03T17:39:47.072000-05:00"
    }
}
```

`aws timestream-write create-table --database-name sir-sim --table-name results`

```
{
    "Table": {
        "Arn": "arn:aws:timestream:us-east-1:[ACCOUNT_ID]:database/sir-sim/table/results",
        "TableName": "results",
        "DatabaseName": "sir-sim",
        "TableStatus": "ACTIVE",
        "RetentionProperties": {
            "MemoryStoreRetentionPeriodInHours": 6,
            "MagneticStoreRetentionPeriodInDays": 73000
        },
        "CreationTime": "2024-12-03T17:41:09.628000-05:00",
        "LastUpdatedTime": "2024-12-03T17:41:09.628000-05:00",
        "MagneticStoreWriteProperties": {
            "EnableMagneticStoreWrites": false
        },
        "Schema": {
            "CompositePartitionKey": [
              ...
            ]
        }
    }
}

```

## Permissions

When setting up Lambda Function, a role needs to be provided to write to Timestream and SQS.

## Input

Results manager runs on AWS Lambda with a SQS trigger.
Expected input was defined within the protobuf file and received as a JSON.

An example:

```

{
results: {
[
{
"time": 1732473550,
"numSusceptible": 100,
"numInfected": 2000,
"numRecovered": 30
}
]
}
}

```

When running in AWS, the following can be used for a test:

```

{
"Records": [
{
"messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
"receiptHandle": "MessageReceiptHandle",
"body": "{\"results\": [{\"results\": [{\"time\": 1732473550000,\"numSusceptible\": 100, \"numInfected\": 2000, \"numRecovered\": 30 }]}]}",
"attributes": {
"ApproximateReceiveCount": "1",
"SentTimestamp": "1523232000000",
"SenderId": "123456789012",
"ApproximateFirstReceiveTimestamp": "1523232000001"
},
"messageAttributes": {},
"md5OfBody": "{{{md5_of_body}}}",
"eventSource": "aws:sqs",
"eventSourceARN": "arn:aws:sqs:us-east-1:123456789012:results",
"awsRegion": "us-east-1"
}
]
}

```

## Developer Notes

Run unit tests:
`python -m unittest .\test_time_stream.py`

To build image:
docker build --tag sir-sim/results-manager .

To run docker image locally:
docker run [environment_variables] -p 9000:8080 sir-sim/results-manager

```

```

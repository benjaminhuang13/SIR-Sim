import json
import boto3

text_event = {
    "api": "post",
    "pop_size": "101",
    "initial_infection_rate": "1",
    "initial_number_of_infected": "1",
    "recovery_rate": "1"
}

sqs_client = boto3.client("sqs")
engine_queue_url  = "https://sqs.us-east-1.amazonaws.com/471112517107/sirsim-engine"

def lambda_handler(event, context):
    data = json.loads(event['body'])
    print('event: ')
    print(event['body'])

    if data['api'] == 'post':
        print('post endpoint called!')
        response = sqs_client.send_message( 
            QueueUrl=engine_queue_url,
            MessageAttributes={
                'source': {
                    'DataType': 'String',
                    'StringValue': 'sirsim-api gateway lambda handler'
                },
                'Author': {
                    'DataType': 'String',
                    'StringValue': 'ben huang'
                }
            },
            MessageBody=json.dumps(data)
        )

        print(response['MessageId'])
    elif data['api'] == 'get':
        print('TODO: get data')

    response_code = 201
    # Only return the sent data in the body if creation was successful
    if (response_code == 201):
        body = json.dumps(data)
    else:
        body = None

    response = {
        "statusCode": response_code,
        "headers": {
        "Access-Control-Allow-Origin" : "*",
        "Access-Control-Allow-Credentials" : "true",
        "Content-Type": "application/json"
        },
        "body": body
    }
    return response
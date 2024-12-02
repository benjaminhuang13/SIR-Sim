import json
import boto3
from botocore.exceptions import ClientError

results_success_queue  = "https://sqs.us-east-1.amazonaws.com/471112517107/results-success"
sqs_client = boto3.client("sqs")

def lambda_handler(event, context):
    try:
        # Receive a message from the SQS queue
        response = sqs_client.receive_message(
            QueueUrl=results_success_queue,
            MaxNumberOfMessages=10,  # Retrieve X messages at a time
            WaitTimeSeconds=7   # Long polling max 20 seconds
        )
        print('response: {}'.format(response))
        if 'Messages' not in response:
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*',  
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
                },
                'body': json.dumps({'message': 'No messages in the queue'})
            }
        message = response['Messages'][-1]
        message_body = message['Body']
        # Delete the message from the queue after processing
        del_res = sqs_client.delete_message(
            QueueUrl=results_success_queue,
            ReceiptHandle=message['ReceiptHandle']
        )
        print('\n\ngot message from sqs: {}\n\n'.format(message_body))
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Message retrieved from SQS',
                'headers': {
                    'Access-Control-Allow-Origin': '*',  
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
                },
                'data': message_body
            })
        }
    except ClientError as e:
        print(f"Error receiving or deleting message from SQS: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
                },
            'body': json.dumps({'message': 'Internal server error'})
        }
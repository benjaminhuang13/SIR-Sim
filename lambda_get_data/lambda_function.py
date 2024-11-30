import json
import boto3
from botocore.exceptions import ClientError

test_event = {
    "api": "post",
    "pop_size": "555",
    "initial_infection_rate": "1",
    "initial_number_of_infected": "1",
    "recovery_rate": "1"
}
results_success_queue  = "https://sqs.us-east-1.amazonaws.com/471112517107/results-success"
sqs_client = boto3.client("sqs")

def lambda_handler(event, context):
    try:
        # Receive a message from the SQS queue
        response = sqs_client.receive_message(
            QueueUrl=results_success_queue,
            MaxNumberOfMessages=10,  # Retrieve one message at a time
            WaitTimeSeconds=1      # Long polling for 10 seconds
        )
        print('response: {}'.format(response))
        if 'Messages' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'No messages in the queue'})
            }
        message = response['Messages'][0]
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
                'data': message_body
            })
        }
    except ClientError as e:
        print(f"Error receiving or deleting message from SQS: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error'})
        }
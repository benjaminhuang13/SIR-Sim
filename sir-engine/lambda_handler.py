import json
import boto3
from sir_simulation import sir_simulation
import os

# Initialize SQS client
sqs = boto3.client('sqs')
OUTPUT_QUEUE_URL = os.environ.get('OUTPUT_QUEUE', 'errorVal')

def lambda_handler(event, context):
    try:
        results = []
        for record in event['Records']:
            body = json.loads(record['body'])  # Parse the message body
            if not body:
                print(f"Warning: Empty body in record: {record}")
                continue
            user_inputs = body.get('userInputs')

            try:
                population_size = user_inputs['populationSize']
                infection_rate = user_inputs['infectionRate']
                num_infected = user_inputs['numInfected']
                recovery_rate = user_inputs['recoveryRate']
                time_steps = user_inputs['timeStepsDays']
            except:
                if user_inputs:
                    result = { "results": f"malformed input: {user_inputs}" }
                    results.append(result)
                    continue
                else:
                    result = { "results": f"malformed input: key 'user_inputs' not found in input json" }
                    results.append(result)
                    continue

            # Run SIR simulation
            sim_results = sir_simulation(population_size, infection_rate, num_infected, recovery_rate, time_steps)
            result = { "results": sim_results }
            results.append(result)

            # Send the result to the output SQS queue
            sqs.send_message( QueueUrl=OUTPUT_QUEUE_URL, MessageBody=json.dumps(result) )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
                },
            'body': json.dumps({'message': 'Successful execution'})
            }
    except Exception as e:        
        print('something wrong happened: {}'.format(e))
        return {
            'statusCode': 204,
            'headers': {
                'Access-Control-Allow-Origin': '*',  
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
                },
            'body': json.dumps({'message': 'something wrong happened, check logs'})
            }
    
import json
import boto3
from sir_simulation import sir_simulation
import os

# Initialize SQS client
sqs = boto3.client('sqs')
OUTPUT_QUEUE_URL = os.environ.get('OUTPUT_QUEUE', 'errorVal')

def lambda_handler(event, context):
    try:
        print("event: {}".format(event))
        results = []
        body = json.loads(event['body'])  # Parse the message body
        if not body:
            print(f"Warning: Empty body in record: {event}")
        else:
            print("body: {}".format(body))
        user_inputs = body['userInputs']

        try:
            population_size = int(user_inputs['populationSize'])
            infection_rate = float(user_inputs['infectionRate'])
            num_infected = float(user_inputs['numInfected'])
            recovery_rate = float(user_inputs['recoveryRate'])
            time_steps = int(user_inputs['timeStepsDays'])
        except:
            if user_inputs:
                result = { "results": f"malformed input: {user_inputs}" }
                results.append(result)
                print("malformed input: {}".format(user_inputs))
            else:
                result = { "results": f"malformed input: key 'user_inputs' not found in input json" }
                results.append(result)
                print("malformed input: key 'user_inputs' not found in input jso")

        # Run SIR simulation
        sim_results = sir_simulation(population_size, infection_rate, num_infected, recovery_rate, time_steps)
        result = { "results": sim_results }
        results.append(result)
        print('result: {}'.format(result))
        print('results: {}'.format(results))
        # Send the result to the output SQS queue
        sqs.send_message( QueueUrl=OUTPUT_QUEUE_URL, MessageBody=json.dumps(result) )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
                },
            'body': json.dumps({'message': 'Successful execution!'})
            }
    except Exception as e:        
        print('Something wrong happened: {}'.format(e))
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
                },
            'body': json.dumps({'message': 'Something wrong happened, check logs'})
            }
    
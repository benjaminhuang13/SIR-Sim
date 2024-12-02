import json
from sir_simulation import sir_simulation
from datetime import datetime, timedelta
import os
import boto3

# Initialize SQS client
sqs = boto3.client('sqs')
OUTPUT_QUEUE_URL = os.environ.get('OUTPUT_QUEUE', 'errorVal')   


def lambda_handler(event, context):
    try:
        # Parse body from the API Gateway event
        body = json.loads(event.get('body', '{}'))
        print(type(body))
        print(body)
        
        if 'userInputs' not in body:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS, POST, PUT'
                },
                'body': json.dumps({'message': "Missing 'userInputs' in request body"})
            }
        
        # Extract user inputs
        user_inputs = body['userInputs']
        
        try:
            # Validate and convert inputs
            population_size = int(user_inputs['populationSize'])
            infection_rate = float(user_inputs['infectionRate'])
            num_infected = int(user_inputs['numInfected'])
            recovery_rate = float(user_inputs['recoveryRate'])
            time_steps = int(user_inputs['timeStepsDays'])
        except KeyError as e:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS, POST, PUT'
                },
                'body': json.dumps({'message': f"Missing or invalid parameter: {str(e)}"})
            }
        
        # Run the SIR simulation
        simulation_results = sir_simulation(population_size, infection_rate, num_infected, recovery_rate, time_steps)
        print(type(simulation_results))
        result = { "results": simulation_results }
        print('simulation_results: {}'.format(simulation_results))
        # Send the result to the output SQS queue
        sqs.send_message( QueueUrl=OUTPUT_QUEUE_URL, MessageBody=json.dumps(result))

        # Return results
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS, POST, PUT'
            },
            'body': json.dumps(simulation_results)
        }
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS, POST, PUT'
            },
            'body': json.dumps({'message': 'Internal server error'})
        }

import json
from sir_simulation import sir_simulation

def lambda_handler(event, context):
    user_inputs = event.get('userInputs') # Parse user inputs from the event

    population_size = user_inputs['populationSize']
    infection_rate = user_inputs['infectionRate']
    num_infected = user_inputs['numInfected']
    recovery_rate = user_inputs['recoveryRate']
    time_steps = user_inputs['timeStepsDays']
    
    # SIR simulation using Cython function
    sim_results = sir_simulation(population_size, infection_rate, num_infected, recovery_rate, time_steps)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'results': sim_results})
    }

import numpy as np
from datetime import datetime, timedelta

def sir_simulation(population_size, infection_rate, num_infected, recovery_rate, time_steps):
    # Initialize variables
    num_susceptible = population_size - num_infected
    num_recovered = 0

    results = []

    for day in range(time_steps):
        # Calculate new infections and recoveries
        new_infections = int(infection_rate * num_susceptible * num_infected / population_size)
        new_recoveries = int(recovery_rate * num_infected)

        # Prevent values from becoming negative
        new_infections = min(new_infections, num_susceptible)
        new_recoveries = min(new_recoveries, num_infected)

        # Update states
        num_susceptible -= new_infections
        num_infected = num_infected + new_infections - new_recoveries
        num_recovered = population_size - num_susceptible - num_infected

        # Prevent negative infected values (edge case handling)
        num_infected = max(num_infected, 0)

        # Record results
        epoch_time = int((datetime.now() + timedelta(days=day)).timestamp()) + 84600
        results.append({
            'time': epoch_time,
            'numSusceptible': num_susceptible,
            'numInfected': num_infected,
            'numRecovered': num_recovered,
        })

    return results

import numpy as np
from datetime import datetime, timedelta
cimport numpy as np

def sir_simulation(int population_size, double infection_rate, int num_infected, double recovery_rate, int time_steps):
    cdef int num_susceptible = population_size - num_infected
    cdef int num_recovered = 0
    cdef int new_infections, new_recoveries

    results = []
    
    for day in range(time_steps):

        new_infections = int(infection_rate * num_susceptible * num_infected / population_size)
        new_recoveries = int(recovery_rate * num_infected)

        num_susceptible = max(num_susceptible - new_infections, 0)
        num_infected = max(num_infected + new_infections - new_recoveries, 0)
        num_recovered = population_size - num_susceptible - num_infected
        
        results.append({
            'time': (datetime.now() + timedelta(days=day)).isoformat(),
            'numSusceptible': num_susceptible,
            'numInfected': num_infected,
            'numRecovered': num_recovered,
        })
    
    return results

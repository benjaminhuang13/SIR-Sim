# SIR-Sim

Webapp hosted on AWS using serverless services. The webapp simulate the effects of certain epidemic parameters on the evolution of a disease. "SIR" stands for "Susceptible, Infected, Recovered" and is a common epidemiological model on which this simulator is based on.

![diagram](/diagram.png)

## sir-engine

Lambda that handles the simulation of data

## sir-results-management

Lambda that handles the archiving of data to Timestream and sends results to SQS

## frontend

HTTML/CSS/Javascript webpage hosted on a S3 bucket

## sir-get-data

Lambda that handles the retrieval of results from an SQS

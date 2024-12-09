# SIR-Sim

Webapp hosted on AWS using serverless services. The webapp simulate the effects of certain epidemic parameters on the evolution of a disease. "SIR" stands for "Susceptible, Infected, Recovered" and is a common epidemiological model on which this simulator is based on.
![demo](/demo.gif)

![diagram](/diagram.png)

## sir-engine

Lambda that handles the simulation of data. See README.md in `/sir-engine` for details about deploying.

## sir-results-management

Lambda that handles the archiving of data to Timestream and sends results to SQS. See README.md in `/sir-results-management` for details about deploying.

## sir-get-data

Lambda that handles the retrieval of results from an SQS. See README.md in `/sir-get-data` for details about deploying.

## frontend

HTTML/CSS/Javascript webpage hosted on a S3 bucket. See README.md in `/frontend` for details about deploying S3 bucket and API Gateway.

### Inspiration
https://itp.uni-frankfurt.de/~gros/StudentProjects/Projects_2020/projekt_benedikt_gutsche/

# SIR-Sim

![diagram](/diagram.png)

## sir-engine

Lambda that handles the simulation of data

## sir-results-management

Lambda that handles the archiving of data to Timestream and sends results to SQS

## frontend

HTTML/CSS/Javascript webpage hosted on a S3 bucket

## sir-get-data

Lambda that handles the retrieval of results from an SQS

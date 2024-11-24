FROM public.ecr.aws/lambda/python:3.8

RUN pip install boto3 

ENV AWS_REGION='us-east-1'
ENV DATABASE_NAME='sir-sim-results'
ENV TABLE_NAME='results'

COPY time_stream_interface.py .
COPY lambda_handler.py .
COPY sqs_handler.py .

# Set to run Lambda handler
CMD ["lambda_handler.lambda_handler"]
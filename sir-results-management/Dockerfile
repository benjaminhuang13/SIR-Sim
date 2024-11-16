FROM public.ecr.aws/lambda/python:3.8

RUN yum install -y gcc python3-devel
RUN pip install boto3 

ENV AWS_REGION='us-east-1'
ENV DATABASE_NAME='sir-sim-results'
ENV TABLE_NAME='results'

COPY messages_pb2.py .
COPY time_stream_interface.py .
COPY lambda_handler.py .

# Set to run Lambda handler
CMD ["lambda_handler.lambda_handler"]
FROM public.ecr.aws/lambda/python:3.8

RUN yum install -y gcc python3-devel
RUN pip install boto3 

ENV REGION 'us-east-1'
ENV DATABASE_NAME 'sir-sim-results'
ENV TABLE_NAME 'results'

COPY time_stream_interface.py .
COPY setup.py .
COPY lambda_handler.py .

# Set to run Lambda handler
CMD ["lambda_handler.lambda_handler"]
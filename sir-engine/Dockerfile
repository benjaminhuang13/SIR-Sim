FROM public.ecr.aws/lambda/python:3.8

ENV OUTPUT_QUEUE=https://sqs.us-east-2.amazonaws.com/851725186983/SQS_OUTPUT

RUN yum install -y gcc python3-devel
RUN pip install numpy
RUN pip install cython
RUN pip install boto3

COPY sir_simulation.pyx .
COPY setup.py .

# compile Cython
RUN python setup.py build_ext --inplace

COPY lambda_handler.py .

# Set to run Lambda handler
CMD ["lambda_handler.lambda_handler"]
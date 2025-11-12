FROM public.ecr.aws/lambda/python:3.10

# Copy function code
COPY main.py requirements.txt ${LAMBDA_TASK_ROOT}/

# Install dependencies
RUN pip install -r requirements.txt

# Set the CMD to your handler (could be main.handler)
CMD ["main.handler"]

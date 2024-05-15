FROM public.ecr.aws/lambda/python:3.12

COPY CreateUser.py requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

CMD ["CreateUser.lambda_handler"]
FROM public.ecr.aws/lambda/python:3.12

COPY DeleteFile.py requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

CMD ["DeleteFile.lambda_handler"]
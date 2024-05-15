FROM public.ecr.aws/lambda/python:3.12

COPY UploadFile.py requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

CMD ["UploadFile.lambda_handler"]
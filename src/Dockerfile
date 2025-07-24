ARG PYTHON_VESSION=3.13
FROM public.ecr.aws/lambda/python:${PYTHON_VESSION}

COPY requirements.txt .

RUN pip3 install -r requirements.txt --target "{LAMBDA_TASK_ROOT}"

WORKDIR ${LAMBDA_TASK_ROOT}

ADD cdk_docker_demo/ cdk_docker_demo

CMD []

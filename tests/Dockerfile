FROM python:3.6-alpine

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY tests/requirements.txt /requirements-tests.txt
RUN pip install -r /requirements-tests.txt

WORKDIR /workspace

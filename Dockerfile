FROM python:3.9.16-alpine3.17

RUN pip install requests

COPY . /src
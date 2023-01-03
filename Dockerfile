FROM alpine:latest AS builder

WORKDIR /src

RUN apk add --update \
    wget \
    unzip

COPY ./get_testfiles.sh /src
RUN chmod 777 ./get_testfiles.sh && ./get_testfiles.sh

FROM python:3.9.16-alpine3.17 AS runner

WORKDIR /src

RUN pip install requests
RUN pip install prometheus_client

COPY . /src

COPY --from=builder /src/test_files/* ./test_files/

RUN echo 'Test files:'
RUN ls test_files

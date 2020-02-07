FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN addgroup -S app && adduser -S -G app app


RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add --no-cache postgresql-dev bash 
COPY ./migrations/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY --chown=app ./migrations /
COPY --chown=app ./core /core
RUN pip install --no-cache-dir /core && \
    rm -fr /core

RUN chmod +x /entrypoint.sh
USER app

WORKDIR /migrations

ENV PYTHONPATH=/migrations
ENTRYPOINT ["/entrypoint.sh"]
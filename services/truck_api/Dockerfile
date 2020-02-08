FROM python:3.6-alpine

RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev && \
    apk add --no-cache postgresql-dev bash
COPY ./services/truck_api/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

ENV PYTHONUNBUFFERED 1

COPY ./services/truck_api /app
RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/gunicorn.sh
COPY ./core /core
RUN pip install -e /core

WORKDIR /app

ENTRYPOINT ["/app/entrypoint.sh"]
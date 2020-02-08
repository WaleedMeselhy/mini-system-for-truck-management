FROM python:3.6-alpine


COPY ./services/celery_worker/requirements.txt /tmp/requirements.txt
RUN apk update && \
    apk add --virtual .build-deps gcc python3-dev musl-dev libxml2-dev libxml2 && \
    apk add libxslt-dev postgresql-dev && \
    pip install --prefer-binary -r /tmp/requirements.txt && \
    rm -r /root/.cache && \
    apk del .build-deps


COPY ./services/celery_worker/. /app
RUN chmod +x /app/entrypoint.sh
WORKDIR /app

COPY ./core /core
RUN pip install -e /core

# ENTRYPOINT [ "/bin/sh", "-c","while true; do sleep 30; done;"]

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python","-m" ,"celery", "-A", "celery_factory","worker","--beat", "--loglevel=info"]
# CMD ["celery","celery", "-A", "celery_factory", "worker", "--loglevel=info"]
# CMD ["/bin/sh","-c","while true; do sleep 30; done;"]
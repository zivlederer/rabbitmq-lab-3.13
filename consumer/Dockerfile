FROM python:3.9-slim
WORKDIR /app
COPY consumer.py /app/
RUN pip install celery
CMD ["celery", "-A", "consumer", "worker", "--loglevel=info"]

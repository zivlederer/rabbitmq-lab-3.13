FROM python:3.9-slim
WORKDIR /app
COPY producer.py /app/
RUN pip install flask celery
CMD ["python", "producer.py"]

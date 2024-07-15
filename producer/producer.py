from flask import Flask, request
from celery import Celery
from kombu import Queue, Exchange
import os

app = Flask(__name__)

rabbitmq_host = os.getenv('RABBITMQ_HOST', 'production-rabbitmqcluster')
celery = Celery('tasks', broker=f'amqp://guest:guest@{rabbitmq_host}:5672//', backend='rpc://')

exchange = Exchange('classic_exchange', type='direct')

celery.conf.update(
    task_default_queue='classic_queue_ziv',
    task_queues=(
        Queue('classic_queue_ziv', exchange=exchange, routing_key='classic_queue_ziv',
              queue_arguments={'ha-mode': 'all'}),
    ),
    task_default_exchange='classic_exchange',
    task_default_routing_key='classic_queue_ziv'
)

@app.route('/produce', methods=['POST'])
def produce():
    data = request.json
    task = add_task.delay(data['a'], data['b'])
    return f"Task sent with id: {task.id}", 202

@celery.task(name='tasks.add')
def add_task(a, b):
    return a + b

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

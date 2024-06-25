from flask import Flask, request
from celery import Celery
import os

app = Flask(__name__)

rabbitmq_host = os.getenv('RABBITMQ_HOST', 'production-rabbitmqcluster')

celery = Celery('tasks', broker=f'amqp://guest:guest@{rabbitmq_host}:5672//', backend='rpc://')

celery.conf.update(
    task_default_queue='quorum_queue_ziv',
    task_queues={
        'quorum_queue_ziv': {
            'type': 'quorum',
            'durable': True,
            'x-quorum-initial-group-size': 3
        }
    }
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
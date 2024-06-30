from celery import Celery
from kombu import Queue, Exchange
import os

rabbitmq_host = os.getenv('RABBITMQ_HOST', 'production-rabbitmqcluster')
app = Celery('tasks', broker=f'amqp://guest:guest@{rabbitmq_host}:5672//', backend='rpc://')

exchange = Exchange('quorum_exchange', type='direct')

app.conf.update(
    task_default_queue='quorum_queue_ziv',
    task_queues=(
        Queue('quorum_queue_ziv', exchange=exchange, routing_key='quorum_queue_ziv',
              queue_arguments={'x-queue-type': 'quorum', 'x-quorum-initial-group-size': 3}),
    ),
    task_default_exchange='quorum_exchange',
    task_default_routing_key='quorum_queue_ziv',
    worker_prefetch_multiplier=1  # Disable global QoS setting
)

@app.task(name='tasks.add')
def add_task(a, b):
    result = a + b
    print(f"Task executed: {a} + {b} = {result}")
    return result

if __name__ == '__main__':
    app.worker_main(['worker', '--queues=quorum_queue_ziv', '--loglevel=info'])

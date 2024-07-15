from celery import Celery
from kombu import Queue, Exchange
import os

rabbitmq_host = os.getenv('RABBITMQ_HOST', 'production-rabbitmqcluster')
app = Celery('tasks', broker=f'amqp://guest:guest@{rabbitmq_host}:5672//', backend='rpc://')

exchange = Exchange('classic_exchange', type='direct')

app.conf.update(
    task_default_queue='classic_queue_ziv',
    task_queues=(
        Queue('classic_queue_ziv', exchange=exchange, routing_key='classic_queue_ziv',
              queue_arguments={'ha-mode': 'all'}),
    ),
    task_default_exchange='classic_exchange',
    task_default_routing_key='classic_queue_ziv',
    worker_prefetch_multiplier=1  # Disable global QoS setting
)

@app.task(name='tasks.add')
def add_task(a, b):
    result = a + b
    print(f"Task executed: {a} + {b} = {result}")
    return result

if __name__ == '__main__':
    app.worker_main(['worker', '--queues=classic_queue_ziv', '--loglevel=info'])

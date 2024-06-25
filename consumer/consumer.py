from celery import Celery
import os

rabbitmq_host = os.getenv('RABBITMQ_HOST', 'production-rabbitmqcluster')

app = Celery('tasks', broker=f'amqp://guest:guest@{rabbitmq_host}:5672//', backend='rpc://')

app.conf.update(
    task_default_queue='quorum_queue_ziv',
    task_queues={
        'quorum_queue_ziv': {
            'type': 'quorum',
            'durable': True,
            'x-quorum-initial-group-size': 3
        }
    }
)

@app.task(name='tasks.add')
def add_task(a, b):
    result = a + b
    print(f"Task executed: {a} + {b} = {result}")
    return result

if __name__ == '__main__':
    app.worker_main(['worker', '-Q', 'quorum_queue_ziv', '--loglevel=info'])
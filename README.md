# What u need to start with RabbitMQ

Yoy can use celery, it's a simple way to connect project to RabbitMQ. And you can user consumer and producer files for raw connection to RabbitMQ.

## You need to download (for Linux):

### RABBITMQ OS

1. Update system: ```sudo apt-get update```
2. Download rabbitmq server to system: ```sudo apt-get install rabbitmq-server```
3. Start rabbitmq server: ```sudo systemctl status rabbitmq-server```

### PYTHON VENV

1. Download celery: ```pip install celery```
2. Download amqp: ```pip install amqp```

<br>

## CELERY WAY

**Set Celery configuration:**

<br>

myproject/celery.py

<br>

```

from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
```
<br>


myproject/settings.py

<br>

```
CELERY_BROKER_URL = 'amqp://localhost'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'rpc://'```
```
<br>

**Start Celery Beat, Worker:** 
1. ```celery -A myproject worker --loglevel=info```
2. ```celery -A myproject beat --loglevel=info```

## RAW CONNECTION WAY

**Create the next 2 files:** ```consumer.py``` and ```producer.py```

**consumer** - file which consumes/reads messages

**producer** - file which produces/writes messages

<br>

**Base consumer/producer for RabbitMQ**

consumer.py:

```
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='order-queue', durable=True)

def callback(ch, method, properties, body):

    print(f'Received message:{body.decode()}')

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='order-queue', on_message_callback=callback, auto_ack=False) # takes message from queue

print('Waiting for the message...')

channel.start_consuming()
```

<br>

producer.py:

```
import pika


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='order-queue', durable=True)


message = 'Hello, RabbitMQ!'

channel.basic_publish(
    exchange='',
    routing_key='order-queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,
    )
) # send message to queue

print(f"Sent message: {message}")

channel.close()
```
**Start Consumer, Producer:** 
1. ```python3 consumer.py```
2. ```python3 producer.py```

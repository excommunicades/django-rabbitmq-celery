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
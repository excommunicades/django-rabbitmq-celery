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
import pika
import json

def callback(ch, method, properties, body):
    print("Received message from queue:")
    print(json.loads(body))
    # Add your processing logic here

def consume_from_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='direct_exchange', exchange_type='direct')
    channel.queue_declare(queue='data_queue', durable=True)
    channel.queue_bind(exchange='direct_exchange', queue='data_queue', routing_key='#')  # Binding to all routing keys
    channel.basic_consume(queue='data_queue', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    consume_from_queue()

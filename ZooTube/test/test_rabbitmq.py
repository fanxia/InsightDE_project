# Test of rabbitmq

import pika,pickle

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

def callback(ch, method, properties, body):
    print(" [x] Received %r" % pickle.loads(body)['count'])
#    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.queue_declare(queue='frame_queue')
channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue='frame_queue', on_message_callback=callback, auto_ack=True)

channel.start_consuming()

import pika


connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()


channel.queue_delete(queue='frame_queue')

connection.close()

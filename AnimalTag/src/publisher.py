import cv2,time,pickle


def publisher(channel,q_name,video_path):
    print('starting...')
    cap = cv2.VideoCapture(video_path)
    fps=cap.get(cv2.CAP_PROP_FPS)
    count = 10
    print('fps:',fps)
    while count<25 and cap.isOpened():
        timestamp=10*count
        cap.set(cv2.CAP_PROP_POS_FRAMES,fps*timestamp)
        ret,frame = cap.read()
        channel.basic_publish(
            exchange='',
            routing_key=q_name,
            body=pickle.dumps({'buff':frame,'timestamp':timestamp})
            )
        print('sent:',count)
        count+=1
        time.sleep(5)
    connection.close()
    cap.release()
    cv2.destroyAllWindows()
    print('ending...')

if __name__=='__main__':
    import json,pika
    with open('config.json') as config_file:
        cfg = json.load(config_file)
    credentials = pika.PlainCredentials(cfg["rabbitmq"]["mq_user"], cfg["rabbitmq"]["mq_passwd"])
    parameters = pika.ConnectionParameters(cfg["rabbitmq"]["mq_host"],cfg["rabbitmq"]["mq_port"],'/',credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=cfg["rabbitmq"]["mq_name"])
    publisher(channel,cfg["rabbitmq"]["mq_name"],"./videotest.mp4")

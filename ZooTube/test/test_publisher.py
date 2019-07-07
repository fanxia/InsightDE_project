# Test of publishing process

import cv2,sys,time
import pika,pickle

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='frame_queue')
print('starting...')
video_path = "./videotest.mp4"
cap = cv2.VideoCapture(video_path)
fps=cap.get(cv2.CAP_PROP_FPS)
count = 10
print('fps:',fps)
while count<25 and cap.isOpened():
    cap.set(cv2.CAP_PROP_POS_FRAMES,fps*10*count)
    ret,frame = cap.read()
    channel.basic_publish(
        exchange='',
        routing_key='frame_queue',
        body=pickle.dumps({'buff':frame,'count':count})
        )
    print('sent:',count)
    count+=1
    time.sleep(5)
connection.close()

cap.release()
cv2.destroyAllWindows()  # destroy all the opened windows

print('ending...')

#! /bin/env python3
'''
This is the file defining the function to read video, 
pre-process frames and publish to rabbitMQ.
'''

import cv2,time,pickle
import json
from util import connect_util

def publisher(channel,q_name,video_path,timestamp=0,timeinterval=1):
    '''
    Read video from video_path, process frames with skipping & resizing,
    publish to queue of q_name through channel.
    '''

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.set(cv2.CAP_PROP_POS_FRAMES,int(fps*timestamp))
    skipframes = int(fps*timeinterval - 1)

    while True:
        #cap.set(cv2.CAP_PROP_POS_FRAMES,fps*timestamp)
        ret,frame = cap.read()
        if not ret: break
        if frame.shape[0] > 480: frame = cv2.resize(frame,(640,480))  # resize frame

        # Send frame and timestamp to rabbitMQ
        channel.basic_publish(
            exchange = '',
            routing_key = q_name,
            body = pickle.dumps({'buff':frame,'timestamp':timestamp})
            )

        for i in range(skipframes): cap.grab()                    # skip frames
        timestamp += timeinterval
    cap.release()



if __name__== '__main__':
    
    # Configuration for rabbitMQ using config.json file.
    with open('util/config.json') as config_file:
        cfg = json.load(config_file)
    connecton , channel = connect_util.rabbit_connect(cfg)

    # Run publisher using test video directly
    publisher(channel,cfg["rabbitmq"]["mq_name"],"./videotest.mp4")
    connection.close()

#! /bin/env python3
'''
This file defines the consumer that can run on instance directly or deploy in cluster as docker image.
It reads the frames queued in RabbitMQ, detect animals using numpydarknet, and save the results into 
pre-built mysql database.
'''
import sys,pickle,time
import darknet,json
from util import connect_util

with open('util/config.json') as config_file:
    cfg = json.load(config_file)

cnx , cur = connect_util.mysql_connect(cfg)

net = darknet.load_net(b"/opt/numpydarknet_gpu/cfg/yolov3.cfg", b"/opt/numpydarknet_gpu/yolov3.weights", 0)
meta = darknet.load_meta(b"/opt/numpydarknet_gpu/cfg/coco.data")

aniset={'bear', 'zebra', 'bird', 'horse', 'cat', 'dog', 'elephant','sheep', 'cow', 'giraffe'}

def callback(ch, method, properties, body):
    mdata = pickle.loads(body)
    print('working on timestamp:',mdata['timestamp'])
    result=darknet.detect_np(net, meta, mdata['buff'])
    print(mdata['timestamp'],result)
    dic={}
    #dic['timestamp']=mdata['timestamp']
    for ob in result:
        ani=ob[0].decode()
        if ani in aniset: dic[ani]=max(int(ob[1]*100),dic.get(ani,0))
    if not dic: return
    print(dic)
    for i in dic:
        cur.execute("INSERT INTO anitag "
             "(object,timestamp,confid)"
              "VALUES ('{0}',{1},{2})".format(i,mdata['timestamp'],dic[i]))
    cnx.commit()

_ , channel = connect_util.rabbit_connect(cfg)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=cfg["rabbitmq"]["mq_name"], on_message_callback=callback, auto_ack=True)
channel.start_consuming()

cur.close()
cnx.close()

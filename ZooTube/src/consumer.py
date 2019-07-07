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

# connect mysql database
cnx , cur = connect_util.mysql_connect(cfg)

# load darknet for yolo
net = darknet.load_net(b"/opt/numpydarknet_gpu/cfg/yolov3.cfg", b"/opt/numpydarknet_gpu/yolov3.weights", 0)
meta = darknet.load_meta(b"/opt/numpydarknet_gpu/cfg/coco.data")

# Define the animals that will be saved in database
aniset={'bear', 'zebra', 'bird', 'horse', 'cat', 'dog', 'elephant','sheep', 'cow', 'giraffe'}


def callback(ch, method, properties, body):
    '''
    Read the frames queued in rabbitmq,
    run darknet to indentify animals,
    and save results to mysql databases.
    '''
    mdata = pickle.loads(body)
    result = darknet.detect_np(net, meta, mdata['buff'])

    # find the animals with max confid for each animal type in one frame
    dic = {}
    for ob in result:
        ani = ob[0].decode()
        if ani in aniset: dic[ani] = max(int(ob[1]*100),dic.get(ani,0))
    if not dic: return

    # save animal type, timestamp and confid into mysql db
    for i in dic:
        cur.execute("INSERT INTO anitag "
             "(object,timestamp,confid)"
              "VALUES ('{0}',{1},{2})".format(i,mdata['timestamp'],dic[i]))
    cnx.commit()


if __name__ == '__main__':

    # Connect rabbitMQ
    _ , channel = connect_util.rabbit_connect(cfg)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=cfg["rabbitmq"]["mq_name"], on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

    cur.close()
    cnx.close()

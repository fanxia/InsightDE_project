import sys,pickle,pika,time
import darknet,json
import mysql.connector

with open('config.json') as config_file:
    cfg = json.load(config_file)

mysqlconfig = {
  'user': cfg['mysql']['db_user'],
  'password': cfg['mysql']['db_passwd'],
  'host': cfg['mysql']['db_host'],
  'database': cfg['mysql']['db_name'],
  'port' : cfg['mysql']['db_port'],
  'raise_on_warnings': True
}
cnx = mysql.connector.connect(**mysqlconfig)
cur = cnx.cursor()
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

credentials = pika.PlainCredentials(cfg["rabbitmq"]["mq_user"], cfg["rabbitmq"]["mq_passwd"])
parameters = pika.ConnectionParameters(cfg["rabbitmq"]["mq_host"],cfg["rabbitmq"]["mq_port"],'/',credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=cfg["rabbitmq"]["mq_name"])
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=cfg["rabbitmq"]["mq_name"], on_message_callback=callback, auto_ack=True)
#channel.basic_consume(queue='frame_queue', on_message_callback=callback)

channel.start_consuming()



cur.close()
cnx.close()

import sys,pickle,pika,time
sys.path.append('/Users/fanxia/fx/insight/InsightDE_project/AnimalTag/darknet/python')
import darknet
import mysql.connector
config = {
  'user': 'root',
  'password': '1990740115',
  'host': '127.0.0.1',
  'database': 'test',
  'raise_on_warnings': True
}
cnx = mysql.connector.connect(**config)
cur = cnx.cursor()
net = darknet.load_net(b"/Users/fanxia/fx/insight/InsightDE_project/AnimalTag/darknet/cfg/yolov3.cfg", b"/Users/fanxia/fx/insight/InsightDE_project/AnimalTag/darknet/yolov3.weights", 0)
meta = darknet.load_meta(b"/Users/fanxia/fx/insight/InsightDE_project/AnimalTag/darknet/cfg/coco.data")

def callback(ch, method, properties, body):
    mdata = pickle.loads(body)
    print('working on count:',mdata['count'])
    #time.sleep(20)

    result=darknet.detect_np(net, meta, mdata['buff'])
    print(mdata['count'],result)
    dic={'bear':0, 'zebra':0}
    for ob in result:
        ani=ob[0].decode()
        if ani in dic and dic[ani]<ob[1]*100:
            dic[ani]=int(ob[1]*100)
    sqlhead= ("INSERT INTO anitag "
             "(BEAR, ZEBRA) "
              "VALUES (%(bear)s, %(zebra)s)")
    print(dic)
    cur.execute(sqlhead,dic)
    cnx.commit()

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='frame_queue')
channel.basic_qos(prefetch_count=1)
#channel.basic_consume(queue='frame_queue', on_message_callback=callback, auto_ack=True)
channel.basic_consume(queue='frame_queue', on_message_callback=callback)

channel.start_consuming()



cur.close()
cnx.close()

import cv2,sys
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

##                                                                                                                                                          
cur = cnx.cursor()
#sql= "INSERT INTO anitag (BEAR, ZEBRA) VALUES(33,98)"
#cur.execute(sql)
#cnx.commit()





net = darknet.load_net(b"/Users/fanxia/fx/insight/InsightDE_project/AnimalTag/darknet/cfg/yolov3.cfg", b"/Users/fanxia/fx/insight/InsightDE_project/AnimalTag/darknet/yolov3.weights", 0)
meta = darknet.load_meta(b"/Users/fanxia/fx/insight/InsightDE_project/AnimalTag/darknet/cfg/coco.data")
video_path = "./videotest.mp4"
cap = cv2.VideoCapture(video_path)
fps=cap.get(cv2.CAP_PROP_FPS)
count = 23
print('fps:',fps)
while count<26 and cap.isOpened():
#while cap.isOpened():
    cap.set(cv2.CAP_PROP_POS_FRAMES,fps*10*count)
    ret,frame = cap.read()
    result=darknet.detect_np(net, meta, frame)
    print(count,result)
#    cv2.imshow('window-name',frame)
    cv2.imwrite("frame%d.jpg" % count, frame)
    count = count + 1
    #if count%400==0: print(count)
    #if cv2.waitKey(10) & 0xFF == ord('q'):
    #    break

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



cap.release()
cv2.destroyAllWindows()  # destroy all the opened windows

cnx.commit()
cur.close()
cnx.close()

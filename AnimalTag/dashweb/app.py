import dash,os,json,pika,multiprocessing
from pytube import YouTube
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import myweb
import publisher
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
cnx.autocommit = True
cur = cnx.cursor()
query = 'select object,count(timestamp) from anitag where confid>70 group by object order by count(timestamp) desc'

credentials = pika.PlainCredentials(cfg["rabbitmq"]["mq_user"], cfg["rabbitmq"]["mq_passwd"])
parameters = pika.ConnectionParameters(cfg["rabbitmq"]["mq_host"],cfg["rabbitmq"]["mq_port"],'/',credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=cfg["rabbitmq"]["mq_name"])

ydir='/tmp/AnimalTag'
os.makedirs(ydir, exist_ok=True)
os.system('rm -f {}/*'.format(ydir))

def start_publisher(yvideo):
    cur.execute("truncate table anitag;")
    vfile=yvideo.streams.first()
    vfile.download(output_path=ydir)
    filename='{0}/{1}'.format(ydir,vfile.default_filename)
    publisher.publisher(channel,cfg["rabbitmq"]["mq_name"],filename)

app=dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server
app.title='AnimalTag'
app.config.suppress_callback_exceptions = True

app.layout=html.Div([
    html.Div(myweb.pageindex()),
    dcc.Interval(id='interval-component',interval=myweb.refresh_time*1000,n_intervals=0)
])

@app.callback(
    Output('page_db', 'children'),
    [Input('subm', 'n_clicks'),Input('interval-component', 'n_intervals')]
)
def get_db(subm,n_intervals):
    if subm:
        cur.execute(query)
        return myweb.barplot(n_intervals,list(cur))

@app.callback(
    Output('video_title', 'children'),
    [Input('subm', 'n_clicks')],[State('yrl', 'value')]
)
def rabbit_send(subm,yrl):
    if subm:
        yvideo=YouTube(yrl)
        multiprocessing.Process(target=start_publisher,args=[yvideo]).start()
        return html.H4(children='Animals found in video: "{0}"'.format(yvideo.title))

@app.callback(
    Output('interval-component', 'n_intervals'),
    [Input('subm', 'n_clicks')]
)
def reset_tm(subm):return 0

@app.callback(
    Output('timestps', 'children'),
    [Input('aniplot', 'clickData')],[State('yrl', 'value'),State('timestps', 'children')]
)
def go_tm(aniplot,yrl,tstps):
    if aniplot is None: return tstps
    obj=aniplot['points'][0]['x']
    cur.execute("select timestamp,confid from anitag where object='{}' and confid>70 order by timestamp;".format(obj))
    timep=list(cur)
    return myweb.gettimes(obj,timep,yrl)
    
if __name__=='__main__':
    #app.run_server(debug=True)
    app.run_server(debug=True,host='0.0.0.0', port='80')
    connection.close()

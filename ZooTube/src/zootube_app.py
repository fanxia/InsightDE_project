import dash,os,json,multiprocessing
from pytube import YouTube
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from util import web_template,connect_util
import publisher


with open('util/config.json') as config_file:
    cfg = json.load(config_file)

# connect mysql database
cnx , cur = connect_util.mysql_connect(cfg)
cnx.autocommit = True
query = 'select object,count(timestamp) from anitag where confid>70 group by object order by count(timestamp) desc'

# connect rabbitmq for publisher
connection , channel = connect_util.rabbit_connect(cfg)

# save input video into tmp/
ydir = '/tmp/zootube'
os.makedirs(ydir, exist_ok=True)
os.system('rm -f {}/*'.format(ydir))

def start_publisher(yvideo):
    '''
    Download youtube video,
    start publisher process.
    '''
    vfile = yvideo.streams.first()
    vfile.download(output_path=ydir)
    filename = '{0}/{1}'.format(ydir,vfile.default_filename)
    publisher.publisher(channel,cfg["rabbitmq"]["mq_name"],filename)


# Start building the web application
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server
app.title = 'Zoo-Tube'
app.config.suppress_callback_exceptions = True

app.layout=html.Div([
    html.Div(web_template.pageindex()),
    dcc.Interval(id='interval-component',interval=web_template.refresh_time*1000,n_intervals=0)
])


# Start publishing process with submit of input url
@app.callback(
    Output('video_title', 'children'),
    [Input('subm', 'n_clicks')],[State('yrl', 'value')]
)
def rabbit_send(subm,yrl):
    if subm:
        yvideo=YouTube(yrl)
        multiprocessing.Process(target=start_publisher,args=[yvideo]).start()
        return html.H4(children='Animals found in video: "{0}"'.format(yvideo.title))


# Truncate table from previous run
@app.callback(
    Output('interval-component', 'n_intervals'),
    [Input('subm', 'n_clicks')]
)
def reset_tm(subm):
    cur.execute("truncate table anitag;")
    return 0


# Read database to update barplot
@app.callback(
    Output('page_db', 'children'),
    [Input('subm', 'n_clicks'),Input('interval-component', 'n_intervals')]
)
def get_db(subm,n_intervals):
    if subm:
        cur.execute(query)
        return web_template.barplot(n_intervals,list(cur))

# List timestamps for an animal bar
@app.callback(
    Output('timestps', 'children'),
    [Input('aniplot', 'clickData')],[State('yrl', 'value'),State('timestps', 'children')]
)
def go_tm(aniplot,yrl,tstps):
    if aniplot is None: return tstps
    obj=aniplot['points'][0]['x']
    cur.execute("select timestamp,confid from anitag where object='{}' and confid>70 order by timestamp;".format(obj))
    timep=list(cur)
    return web_template.gettimes(obj,timep,yrl)

    
if __name__=='__main__':

    app.run_server(debug=True,host='0.0.0.0', port='80')
    connection.close()

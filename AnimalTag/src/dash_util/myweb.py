import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

margin_p1=250
margin_p2=70
bkg_clr='#FFFAFA'
ttl_clr='#E9967A'
refresh_time=3
layout_fig=go.Layout(paper_bgcolor='rgb(255,250,250)',plot_bgcolor='rgb(255,250,250)',clickmode='event+select')

def pageindex():
    return html.Div(style={'backgroundColor': bkg_clr}, children=[
    html.Br(),
    html.H1(children='ZooTube',style={'textAlign': 'center','color': ttl_clr}),
    html.Br(),
    html.Div([
        #html.Hr(),
        html.Div(children='Enter the youtube video url'),
        dcc.Input(id="yrl",placeholder='Enter a url here',type='text',value='https://www.youtube.com/watch?v=_rwW8P3BnXE',size='40'),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Div(children="Now get the animal tags!"),
        html.Div(html.Button('Submit',id='subm',n_clicks=0))        
    ],style={'textAlign': 'center','marginLeft': margin_p1,'marginRight': margin_p1}),
    html.Div([
        html.Hr(),
        html.Div(id='video_title'),
        html.Div(id='page_db'),
        html.Div(id='timestps')],
        style={'marginLeft': margin_p1,'marginRight': margin_p1})
    ])

def barplot(n_intervals,dbinfo):
    return html.Div([
        dcc.Graph(id='aniplot',
                  figure={'data':[go.Bar(x=[i[0] for i in dbinfo],y=[i[1] for i in dbinfo])],
                          'layout':layout_fig}
        ),
        html.Div(children='(click on animal bars for details)'),
        html.Div(children="update time: {0}s".format(n_intervals*refresh_time)),
        ])


def gettimes(obj,timep,yrl):
    output=[html.Hr(),
            html.H5(children="Let's find the {}s".format(obj)),
            html.Br()
    ]
    for i in timep:
        output.append(html.A("time stamp: {}s".format(i[0]), href='{0}#t={1}s'.format(yrl,i[0])))
        output.append(("\t(confidence: {}%)".format(i[1])))
        output.append(html.Br())
    output.append(html.Br())
    output.append(html.Br())
    return html.Div(children=output)
    

import dash_daq as daq
import dash
from dash import html, callback, Output, Input, dcc, State
import interfaceUpdater
import redisConector as rc
import redis
import dash_bootstrap_components as dbc
from JSONReader import get_data, get_0310, get_0001, get_currentFL, get_currentFR, get_currentRL, \
    get_currentRR, get_YawRate, get_YawRateRef

client = redis.Redis(host='redis', port=6379, health_check_interval=30, decode_responses=True)
redisConector = rc.redisConector()
pilaId0310=[0,0,0,0,0,0,0,0,0,0]
dash.register_page(__name__)
latchedStatus = {
    "0" : "Event buffer has a new event entry since last upload",
    "1" : "Event buffer is full and has missed at least one event",
    "2" : "Power module over current detected by hardware",
    "3" : "Power module current offset calibration failed",
    "4" : "Power module temperature sensr defective",
    "5" : "Power module temperature has roeached warning level",
    "6" : "Power module temperature has reached error level",
    "7" : "Power module i*t error",
    "8" : "Power module over current detected by software",
    "9" : "Power module pattern data inconsistency",
    "10" : "Dc link over voltage detected by hardware",
    "11" : "Dc link over voltage detected by software",
    "12" : "Dc link undervoltage detectedy by software",
    "13" : "Fault of the other inverter on the same device",
    "14" : "Motor temperature sensor defective",
    "15" : "Motor temperature has reached warning level",
    "16" : "Motor temperature has reached error level",
    "17" : "Motor stator frequency to high",
    "18" : "Board supply voltage error",
    "19" : "Receive PDO timeout",
    "20" : "NMT not in state operational",
    "21" : "Task calculation time overrun",
    "22" : "Net synchronisation error",
    "23" : "Position device signal to low",
    "24" : "Position device signal to high",
    "25" : "Resolver calibration failed",
    "26" : "System error, analog input or motor feedback DMA error",
    "27" : "Interlock open due to open cover sheet",
    "28" : "Gate driver disabled by APPC",
    "29" : "Motor stall error",
    "30" : "Ambient temperature has reached warning level",
    "31" : "Ambient temperature has reached error level"
}

layout = html.Div(id='element-to-hide', style={'display':'none'}),\
         html.Div(
            children=[
            dcc.Interval(
                id='int-component',
                interval=1500, # in milliseconds
                n_intervals=0
            ),
        ],
    ),\
    html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    children=html.Img(src="../assets/Accumulator.jpg", className="pedalbox-logo"),
                                    className="box1"
                                ),
                                html.Div(
                                    children="Accumulator",
                                    className="box2"
                                ),
                                html.Div(
                                    children=daq.Tank(
                                                id='totalVoltage',
                                                min=480,
                                                max=600,
                                                value=546.8,
                                                showCurrentValue=True,
                                                units='V',
                                                color='green',
                                                height=285,
                                                style={'margin-left': '50px'},
                                            ),
                                    className="box4"
                                ),
                                html.Div(
                                    children=daq.Indicator(
                                              id='k1',
                                              label={'label':"K1", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                              color="green",
                                              size=45,
                                              value=True
                                            ),
                                    className="box5"
                                ),
                                html.Div(
                                    children=daq.Indicator(
                                              id='k2',
                                              label={'label':"K2+", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                              color="green",
                                              size=45,
                                              value=True
                                            ),
                                    className="box6"
                                ),
                                html.Div(
                                    children=daq.Indicator(
                                              id='k3',
                                              label={'label':"K3-", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                              color="green",
                                              size=45,
                                              value=True
                                            ),
                                    className="box7"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='cellMinVoltage',
                                            label={'label':"Cell min voltage", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='3.64',
                                            color="black"

                                        ),
                                    className="box8"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='idCellMinVoltage',
                                            label={'label':"ID cell min voltage", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="box9"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='cellMaxVoltage',
                                            label={'label':"Cell max voltage", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"

                                        ),
                                    className="box10"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='idCellMaxVoltage',
                                            label={'label':"ID cell max voltage", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="box11"
                                ),
                            ],
                            className="cornerWrapper"
                        )
                    ],
                    className="box"
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    children=html.Img(src="../assets/ecu.png", className="pedalbox-logo"),
                                    className="box1"
                                ),
                                html.Div(
                                    children="Car Status",
                                    className="box2"
                                ),
                                html.Div(
                                    children=[html.H5('AMS State Machine',
                                            style={'font-weight': 'bold','font-size':'16px'}
                                            ),
                                            html.H5(
                                            id='smAMS',
                                            style={'font-size':'26px'}
                                            ),
                                            html.Br(),
                                            html.H5('AMS Error',
                                            style={'font-weight': 'bold','font-size':'16px'}
                                            ),
                                            html.H5(
                                            id='errorAMS',
                                            style={'font-size':'26px'}
                                            ),
                                            #html.Div(children=[daq.Indicator(label={'label':"Aux 1"},color="green",value=True),
                                            #                    daq.Indicator(label={'label':"Aux 2"},color="green",value=True),
                                            #                    daq.Indicator(label={'label':"Start"},color="green",value=True),
                                            #                    daq.Indicator(label={'label':"Load on"},color="green",value=True),
                                            #                    daq.Indicator(label={'label':"TV"},color="green",value=True),
                                            #                    daq.Indicator(label={'label':"Power"},color="green",value=True),
                                            #],className="inline")
                                    ],
                                    className="box4"
                                ),
                                html.Div(
                                    children=daq.Indicator(
                                              id='IMD',
                                              label={'label':"IMD", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                              color="red",
                                              size=45,
                                              value=True
                                            ),
                                    className="box5"
                                ),
                                html.Div(
                                    children=daq.Indicator(
                                              id='AMS',
                                              label={'label':"AMS", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                              color="red",
                                              size=45,
                                              value=True
                                            ),
                                    className="box7"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='totalPower',
                                            label={'label':"Total Power", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="box6"
                                ),
                                html.Div(
                                    children=[html.H5('Safety',
                                            style={'font-weight': 'bold','font-size':'16px'}
                                            ),
                                            html.H5(
                                            id='safetyLine',
                                            style={'font-size':'26px'}
                                            ),
                                        ],
                                    className="box8"
                                ),
                                html.Div(
                                    children=[html.H5('Safety front',
                                            style={'font-weight': 'bold','font-size':'16px'}
                                            ),
                                            html.H5(
                                            id='safetyFront',
                                            style={'font-size':'26px'}
                                        ),
                                    ],
                                    className="box9"
                                ),
                                html.Div(
                                    children=[html.H5('Car status',
                                            style={'font-weight': 'bold','font-size':'16px'}
                                            ),
                                            html.H5(
                                            id='carStatus',
                                            style={'font-size':'26px'}
                                        ),
                                    ],
                                    className="box11"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='Speed',
                                            label={'label':"Speed", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="box10"
                                ),
                            ],
                            className="cornerWrapper"
                        )
                    ],
                    className="box"
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    children=html.Img(src="../assets/PedalBox.jpg", className="pedalbox-logo"),
                                    className="box1"
                                ),
                                html.Div(
                                    children="Driver Inputs",
                                    className="box2"
                                ),
                                html.Div(
                                    children=[dcc.Graph(
                                        id="grafico-1",
                                        figure={'layout':{"autosize":False}},
                                        style={'width': '100%', 'height':'100%', 'margin':{'l':'0','r':'0','b':'0','t':'0'}, 'margin-top':'-35px'},
                                        config={"responsive":True,"displayModeBar": False, "edits":{"titleText":False,"legendText":False, "annotationPosition":False,"colorbarTitleText":False},"displayModeBar":True},

                                    ),
                                    dcc.Slider( -28, 28, 0.5, value=0,  included=False, id="volante",
                                                    tooltip={"placement": "bottom", "always_visible": True},
                                                    marks={
                                                            0: {'label': '0°', 'style': {'color': '#f50', 'size':'18px'}},

                                                        },
                                               ),
                                    ],
                                    className="box3"
                                )
                            ],
                            className="cornerWrapper"
                        ),
                    ],
                    className="box"
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    children=html.Img(src="../assets/Motor.png", className="pedalbox-logo"),
                                    className="box1"
                                ),
                                html.Div("Drivetrain",
                                    className="box2"
                                ),
                                html.Div(
                                    children=[html.H6('Statusword FL', className='statuswordtit'),
                                              html.H5('A67F', id='sw1'),
                                              #html.Br(style={'display': 'block', 'margin-bottom': '20px'}),
                                              html.H6('Statusword FR', className='statuswordtit'),
                                              html.H5('A67F', id='sw2'),
                                              #html.Br(className='miniBr'),
                                              html.H6('Statusword RL', className='statuswordtit'),
                                              html.H5('A67F', id='sw3'),
                                              #html.Br(className='miniBr'),
                                              html.H6('Statusword RR', className='statuswordtit'),
                                              html.H5('A67F', id='sw4'),
                                              ],
                                    className="box4"
                                ),
                                html.Div(
                                    children=daq.Gauge(
                                    id='SpeedFL',
                                    style={'width': '100%', 'height':'100%', 'margin':{'l':'0','r':'0','b':'0','t':'0'}},
                                    size=160,
                                    label={'label':"Speed FL", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                    color="#e30202",
                                    scale={'start': 0, 'interval': 1000, 'labelInterval': 4},
                                    showCurrentValue=True,
                                    units="RPM",
                                    value=5000,
                                    min=0,
                                    max=20000,
                                    ),
                                    className="box8"
                                ),
                                html.Div(
                                    children=daq.Gauge(
                                    id='SpeedFR',
                                    style={'width': '100%', 'height':'100%', 'margin':{'l':'0','r':'0','b':'0','t':'0'}},
                                    size=160,
                                    label={'label':"Speed FR", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                    color="#e30202",
                                    scale={'start': 0, 'interval': 1000, 'labelInterval': 4},
                                    showCurrentValue=True,
                                    units="RPM",
                                    value=3000,
                                    min=0,
                                    max=20000,
                                    ),
                                    className="box9"
                                ),
                                html.Div(
                                    children=[html.Br(),daq.Gauge(
                                    id='SpeedRL',
                                    style={'width': '100%', 'height':'100%', 'margin':{'l':'0','r':'0','b':'0','t':'50'}},
                                    size=160,
                                    label={'label':"Speed RL", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                    labelPosition='bottom',
                                    color="#e30202",
                                    scale={'start': 0, 'interval': 1000, 'labelInterval': 4},
                                    showCurrentValue=True,
                                    units="RPM",
                                    value=20000,
                                    min=0,
                                    max=20000,
                                    ),],
                                    className="box10"
                                ),
                                html.Div(
                                    children=[html.Br(),daq.Gauge(
                                    id='SpeedRR',
                                    style={'width': '100%', 'height':'100%', 'margin':{'l':'0','r':'0','b':'0','t':'50'}},
                                    size=160,
                                    label={'label':"Speed RR", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                    labelPosition='bottom',
                                    color="#e30202",
                                    scale={'start': 0, 'interval': 1000, 'labelInterval': 4},
                                    showCurrentValue=True,
                                    units="RPM",
                                    value=20000,
                                    min=0,
                                    max=20000,
                                    ),],
                                    className="box11"
                                ),
                            ],
                            className="cornerWrapper"
                        )
                    ],
                    className="box"
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    children=html.Img(src="../assets/Motor.png", className="pedalbox-logo"),
                                    className="box1"
                                ),
                                html.Div(
                                    children="Drivetrain",
                                    className="box2"
                                ),
                                html.Div(
                                    children=[daq.Thermometer(
                                                    id='tempFL',
                                                    value=40,
                                                    height=110,
                                                    min=0,
                                                    max=80,
                                                    showCurrentValue=True,
                                                    style={
                                                        'margin-left': '-80px', 'margin-bottom' : '20px', 'margin-top' : '-40px'
                                                    }
                                                ),
                                                daq.Thermometer(
                                                    id='tempFR',
                                                    value=40,
                                                    height=110,
                                                    min=0,
                                                    max=80,
                                                    showCurrentValue=True,
                                                    style={
                                                        'margin-left' : '-80px', 'margin-top' : '-5 px'
                                                    }
                                                ),
                                                daq.Thermometer(
                                                    id='tempRL',
                                                    value=40,
                                                    height=110,
                                                    min=0,
                                                    max=80,
                                                    showCurrentValue=True,
                                                    style={
                                                        'margin-top': '-455px', 'margin-right' : '-110px'
                                                    }
                                                ),
                                                daq.Thermometer(
                                                    id='tempRR',
                                                    value=40,
                                                    height=110,
                                                    min=0,
                                                    max=80,
                                                    showCurrentValue=True,
                                                    style={
                                                        'margin-top': '10px', 'margin-right' : '-110px'
                                                    }
                                                ),
                                              ],
                                    className="box4"
                                ),
                                html.Div(
                                    children=daq.Gauge(
                                    id='powerFL',
                                    style={'width': '100%', 'height':'100%', 'margin':{'l':'0','r':'0','b':'0','t':'0'}},
                                    size=160,
                                    label={'label':"Power FL", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                    color="#e30202",
                                    showCurrentValue=True,
                                    units="W",
                                    value=0,
                                    min=-524288,
                                    max=524272,
                                    ),
                                    className="box8"
                                ),
                                html.Div(
                                    children=daq.Gauge(
                                    id='powerFR',
                                    style={'width': '100%', 'height':'100%', 'margin':{'l':'0','r':'0','b':'0','t':'0'}},
                                    size=160,
                                    label={'label':"Power FR", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                    color="#e30202",
                                    showCurrentValue=True,
                                    units="W",
                                    value=0,
                                    min=-524288,
                                    max=524272,
                                    ),
                                    className="box9"
                                ),
                                html.Div(
                                    children=[html.Br(),daq.Gauge(
                                    id='powerRL',
                                    style={'width': '100%', 'height':'100%', 'margin':{'l':'0','r':'0','b':'0','t':'50'}},
                                    size=160,
                                    label={'label':"Power RL", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                    labelPosition='bottom',
                                    color="#e30202",
                                    showCurrentValue=True,
                                    units="W",
                                    value=0,
                                    min=-524288,
                                    max=524272,
                                    ),],
                                    className="box10"
                                ),
                                html.Div(
                                    children=[html.Br(),daq.Gauge(
                                    id='powerRR',
                                    style={'width': '100%', 'height':'100%', 'margin':{'l':'0','r':'0','b':'0','t':'50'}},
                                    size=160,
                                    label={'label':"Power RR", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                    labelPosition='bottom',
                                    color="#e30202",
                                    showCurrentValue=True,
                                    units="W",
                                    value=0,
                                    min=-524288,
                                    max=524272,
                                    ),],
                                    className="box11"
                                ),
                            ],
                            className="cornerWrapper"
                        )
                    ],
                    className="box"
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    children=html.Img(src="../assets/Motor.png", className="pedalbox-logo"),
                                    className="box1"
                                ),
                                html.Div(
                                    children=["Drivetrain",dbc.Button("Status Words", id="open", n_clicks=0, color="danger", style={'width': '30%', 'height':'100%', 'margin':{'l':'250px','r':'0','b':'0','t':'0'}}),
                                            dbc.Modal(
                                                [
                                                    dbc.ModalHeader(dbc.ModalTitle("Status Words")),
                                                    dbc.ModalBody( children=html.Div(children=[
                                                            html.Div(children=[daq.Indicator(
                                                                        id="motor1",
                                                                        label=status,
                                                                        labelPosition="right",
                                                                        color="grey",
                                                                        value=False,
                                                                        style={'float' : 'left'}
                                                                        )for status in latchedStatus
                                                            ], className="motor1"),
                                                            html.Div(children=[daq.Indicator(
                                                                        id="motor2",
                                                                        label=status,
                                                                        labelPosition="right",
                                                                        color="grey",
                                                                        value=False,
                                                                        style={'float' : 'left'}
                                                                        )for status in latchedStatus
                                                            ], className="motor2"),
                                                            html.Div(children=[daq.Indicator(
                                                                        id="motor3",
                                                                        label=status,
                                                                        labelPosition="right",
                                                                        color="grey",
                                                                        value=False,
                                                                        style={'float' : 'left'}
                                                                        )for status in latchedStatus
                                                            ], className="motor3"),
                                                            html.Div(children=[daq.Indicator(
                                                                        id="motor4",
                                                                        label=status,
                                                                        labelPosition="right",
                                                                        color="grey",
                                                                        value=False,
                                                                        style={'float' : 'left'}
                                                                        )for status in latchedStatus
                                                            ], className="motor4")],className="contenedorMotores"),
                                                    className="contenedorMotores",
                                                    id='motorContent'),
                                                    dbc.ModalFooter(
                                                        dbc.Button(
                                                            "Cerrar", id="close", className="ms-auto", n_clicks=0, color="danger"
                                                        )
                                                    ),
                                                ],
                                                id="modal",
                                                size="xl",
                                                is_open=False,
                                                fullscreen=True
                                            ),],
                                    className="box2"
                                ),
                                html.Div(
                                    children=[html.H6('LatchedStatus FL', className='statuswordtit'),
                                              html.H5('A67F', id='LS FL'),
                                              #html.Br(style={'display': 'block', 'margin-bottom': '20px'}),
                                              html.H6('LatchedStatus FR', className='statuswordtit'),
                                              html.H5('A67F', id='LS FR'),
                                              #html.Br(className='miniBr'),
                                              html.H6('LatchedStatus RL', className='statuswordtit'),
                                              html.H5('A67F', id='LS RL'),
                                              #html.Br(className='miniBr'),
                                              html.H6('LatchedStatus RR', className='statuswordtit'),
                                              html.H5('A67F', id='LS RR'),
                                              ],
                                    className="box4"
                                ),
                                html.Div(
                                    children=daq.Gauge(
                                    id='tqComFL',
                                    style={'width': '100%', 'height':'100%', 'margin':{'l':'0','r':'0','b':'0','t':'0'}},
                                    size=160,
                                    label={'label':"TorqueCommand FL", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                    color="#e30202",
                                    scale={'start': 0, 'interval': 100, 'labelInterval': 1},
                                    showCurrentValue=True,
                                    value=1000,
                                    min=0,
                                    max=1000,
                                    ),
                                    className="box8"
                                ),
                                html.Div(
                                    children=daq.Gauge(
                                    id='tqComFR',
                                    style={'width': '100%', 'height':'100%', 'margin':{'l':'0','r':'0','b':'0','t':'0'}},
                                    size=160,
                                    label={'label':"TorqueCommand FR", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                    color="#e30202",
                                    scale={'start': 0, 'interval': 100, 'labelInterval': 1},
                                    showCurrentValue=True,
                                    value=1000,
                                    min=0,
                                    max=1000,
                                    ),
                                    className="box9"
                                ),
                                html.Div(
                                    children=[html.Br(),daq.Gauge(
                                    id='tqComRL',
                                    style={'width': '100%', 'height':'100%', 'margin':{'l':'0','r':'0','b':'0','t':'50'}},
                                    size=160,
                                    label={'label':"TorqueCommand RL", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                    labelPosition='bottom',
                                    color="#e30202",
                                    scale={'start': 0, 'interval': 100, 'labelInterval': 1},
                                    showCurrentValue=True,
                                    value=1000,
                                    min=0,
                                    max=1000,
                                    ),],
                                    className="box10"
                                ),
                                html.Div(
                                    children=[html.Br(),daq.Gauge(
                                    id='tqComRR',
                                    style={'width': '100%', 'height':'100%', 'margin':{'l':'0','r':'0','b':'0','t':'50'}},
                                    size=160,
                                    label={'label':"TorqueCommand RR", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                    labelPosition='bottom',
                                    color="#e30202",
                                    scale={'start': 0, 'interval': 100, 'labelInterval': 1},
                                    showCurrentValue=True,
                                    value=1000,
                                    min=0,
                                    max=1000,
                                    ),
                                    ],
                                    className="box11"
                                ),
                            ],
                            className="cornerWrapper"
                        )
                    ],
                    className="box"
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    children=html.Img(src="../assets/Motor.png", className="pedalbox-logo"),
                                    className="box1"
                                ),
                                html.Div(
                                    children="Drivetrain",
                                    className="box2"
                                ),
                                html.Div(
                                    children=dcc.Graph(
                                        id="current-Graph",
                                        figure={'layout':{"autosize":False}},
                                        style={'width': '100%', 'height':'100%', 'margin':{'l':'0','r':'0','b':'0','t':'0'}},
                                        config={"responsive":True,"displayModeBar": False, "edits":{"titleText":False,"legendText":False, "annotationPosition":False,"colorbarTitleText":False},"displayModeBar":True},

                                    ),
                                    className="box3"
                                )



                            ],
                            className="cornerWrapper"
                        )
                    ],
                    className="box"
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    children=html.Img(src="../assets/Motor.png", className="pedalbox-logo"),
                                    className="box1"
                                ),
                                html.Div(
                                    children="Torque Vectoring",
                                    className="box2"
                                ),
                                html.Div(
                                    children=dcc.Graph(
                                        id="YawRate-Graph",
                                        figure={'layout':{"autosize":False}},
                                        style={'width': '100%', 'height':'100%', 'margin':{'l':'0','r':'0','b':'0','t':'0'}},
                                        config={"responsive":True,"displayModeBar": False, "edits":{"titleText":False,"legendText":False, "annotationPosition":False,"colorbarTitleText":False},"displayModeBar":True},

                                    ),
                                    className="box3"
                                )



                            ],
                            className="cornerWrapper"
                        )
                    ],
                    className="box"
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    children=html.Img(src="../assets/Motor.png", className="pedalbox-logo"),
                                    className="box1"
                                ),
                                html.Div(
                                    children="Torque Vectoring",
                                    className="box2"
                                ),
                                html.Div(
                                    children=html.Div(
                                    children=[daq.LEDDisplay(
                                            id='power',
                                            label={'label':"POWER", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"

                                        ),
                                    html.Div(
                                    children=daq.LEDDisplay(
                                            id='TV_Value',
                                            label={'label':"Torque Vectoring", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="box9"
                                ),
                                html.Div(
                                    children=daq.Indicator(
                                              id='tvValue',
                                              label={'label':"TV Running", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                              color="green",
                                              size=45,
                                              value=True
                                            ),
                                    className="box6"
                                ),],
                                    className="box10"
                                ),

                                ),
                                html.Div(
                                    children=daq.Thermometer(
                                                    id='tempFLIGBT',
                                                    value=40,
                                                    height=110,
                                                    min=0,
                                                    max=90,
                                                    showCurrentValue=True,
                                                    style={
                                                        'margin-left' : '-80px', 'margin-top' : '-5 px'
                                                    }
                                                ),
                                ),
                                html.Div(
                                    children=daq.Thermometer(
                                                    id='tempFRIGBT',
                                                    value=40,
                                                    height=110,
                                                    min=0,
                                                    max=90,
                                                    showCurrentValue=True,
                                                    style={
                                                        'margin-left' : '-80px', 'margin-top' : '-5 px'
                                                    }
                                                ),
                                ),
                                html.Div(
                                    children=daq.Thermometer(
                                                    id='tempRLIGBT',
                                                    value=40,
                                                    height=110,
                                                    min=0,
                                                    max=90,
                                                    showCurrentValue=True,
                                                    style={
                                                        'margin-top' : '200px', 'margin-left': '200px'
                                                    }
                                                ),
                                ),
                                html.Div(
                                    children=daq.Thermometer(
                                                    id='tempRRIGBT',
                                                    value=40,
                                                    height=110,
                                                    min=0,
                                                    max=90,
                                                    showCurrentValue=True,
                                                    style={
                                                        'margin-top' : '200px', 'margin-left': '200px'
                                                    }
                                                ),
                                ),



                            ],
                            className="cornerWrapper"
                        )
                    ],
                    className="box"
                )
            ],
            className="container2"
        ),




@callback(
    [Output("grafico-1", "figure"), Output('totalVoltage', 'value'), Output('cellMinVoltage', 'value'), Output('idCellMinVoltage', 'value'), Output('totalVoltage', 'color'), Output('cellMinVoltage', 'color'), Output('cellMaxVoltage', 'value'), Output('idCellMaxVoltage', 'value'), Output('k1', 'color'), Output('k2', 'color'), Output('k3', 'color'), Output("safetyFront", "children"), Output("safetyLine", "children"), Output("carStatus", "children"), Output('sw1', 'children'), Output('sw2', 'children'), Output('sw3', 'children'), Output('sw4', 'children'), Output('SpeedFL','value'), Output('SpeedFR','value'), Output('SpeedRL','value'), Output('SpeedRR','value'), Output('LS FL', 'children'), Output('LS FR', 'children'), Output('LS RL', 'children'), Output('LS RR', 'children'), Output('IMD', 'color'), Output('AMS', 'color'), Output('totalPower', 'value'), Output('tempFL','value'), Output('tempFR','value'), Output('tempRL','value'), Output('tempRR','value'), Output('powerFL','value'), Output('powerFR','value'), Output('powerRL','value'), Output('powerRR','value'), Output('tqComFL','value'), Output('tqComFR','value'), Output('tqComRL','value'), Output('tqComRR','value'), Output('Speed', 'value'), Output('smAMS', 'children'), Output('errorAMS', 'children'), Output("current-Graph", "figure"), Output("YawRate-Graph", "figure"),  Output('volante','value'), Output('power','value'),Output('TV_Value','value'), Output('tvValue', 'color'), Output('tempFLIGBT', 'value'), Output('tempFRIGBT', 'value'), Output('tempRLIGBT', 'value'), Output('tempRRIGBT', 'value')],
    Input('int-component', 'n_intervals'),
)
def acutaliza(N):
    #begining = time.time()
    #print(data)
    #figura2 = interfaceUpdater.updateFigure2(data.get('0310'))

    totalVoltage, minVoltage, idMinVoltage, voltageColor, maxVoltage, idMaxVoltage, minTemp, idMinTemp, maxTemp, idMaxTemp, colorTemp = interfaceUpdater.updateVoltages(redisConector.get_value('0311'))
    k1, k2, k3, smAMS, errorAMS, imd, amsMode, timedOutSlvave, current, amsLed = interfaceUpdater.contactorFeedbackAndAMSState(redisConector.get_value('0310'))

    figura1 = interfaceUpdater.updateFigure1(redisConector.get_value('0001'))

    safetyFront = interfaceUpdater.safetyFront(redisConector.get_value('00a2'))
    safetyValue, imd, ams, plausibility, carState = interfaceUpdater.safety(redisConector.get_value('00f1'), redisConector.get_value('0310'))

    sw1, ls1, sw2, ls2, sw3, ls3, sw4, ls4 = interfaceUpdater.motorData(redisConector.get_value('01cf'), redisConector.get_value('02cf'), redisConector.get_value('01ce'), redisConector.get_value('02ce'))
    speedFL, speedFR, speedRL, speedRR = interfaceUpdater.motorRPM(redisConector.get_value('024f'), redisConector.get_value('034f'), redisConector.get_value('024e'), redisConector.get_value('034e'))
    tempFL, tempFR, tempRL, tempRR, powerFL, powerFR, powerRL, powerRR = interfaceUpdater.powerAndDCVoltage(redisConector.get_value('028f'), redisConector.get_value('038f'), redisConector.get_value('028e'), redisConector.get_value('038e'))
    tqComFL, tqComFR, tqComRL, tqComRR = interfaceUpdater.torqueCommands(redisConector.get_value('020e'), redisConector.get_value('040e'), redisConector.get_value('020f'), redisConector.get_value('040f'))
    speed, yawRateRef = interfaceUpdater.speedAndYawRateRef(redisConector.get_value('00f2'))
    currentFigure = interfaceUpdater.currents(redisConector.get_value('024f'), redisConector.get_value('034f'), redisConector.get_value('024e'), redisConector.get_value('034f'))
    yawRateFigure = interfaceUpdater.updateYawRate(redisConector.get_value('0122'), redisConector.get_value('00f2'))
    steering = interfaceUpdater.updateSteeringWheel(redisConector.get_value('0181'))
    power, torqueValue = interfaceUpdater.dashData(redisConector.get_value('00a2'))
    tvRunning = interfaceUpdater.tvRunning(redisConector.get_value('00f0'))
    totalPower = interfaceUpdater.getTotalPower(redisConector.get_value('00f2'))
    tempIGBTFL, tempIGBTFR, tempIGBTRL, tempIGBTRR = interfaceUpdater.getTempIGBTS(redisConector.get_value('028e'), redisConector.get_value('038e'), redisConector.get_value('028f'), redisConector.get_value('038f'))
    #print("aaaa")
    #print(carState)
    #end = time.time()
    #print(end-begining)
    return figura1, totalVoltage, minVoltage, idMinVoltage, voltageColor, voltageColor, maxVoltage, idMaxVoltage, k1, k2, k3, safetyFront, safetyValue, carState, sw1, sw2, sw3, sw4, speedFL, speedFR, speedRL, speedRR, ls1, ls2, ls3, ls4, imd, ams, totalPower, tempFL, tempFR, tempRL, tempRR, powerFL, powerFR, powerRL, powerRR, tqComFL, tqComFR, tqComRL, tqComRR, speed, smAMS, errorAMS, currentFigure, yawRateFigure, steering, power, torqueValue, tvRunning, tempIGBTFL, tempIGBTFR, tempIGBTRL, tempIGBTRR

@callback(
    [Output("modal", "is_open"), Output("motorContent", "children")],
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    contenido = interfaceUpdater.updateStatuswordTranslation(redisConector.get_value('01cf'), redisConector.get_value('02cf'), redisConector.get_value('01ce'), redisConector.get_value('02ce'))
    if n1 or n2:
        return not is_open, contenido
    return is_open, contenido

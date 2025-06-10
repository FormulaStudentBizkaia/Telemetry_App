import random
from JSONReader import get_0001, get_data
import dash
import dash_daq as daq
import dash_bootstrap_components as dbc
import redisConector as rc
from dash import html, Dash, Input, ctx, Output, dcc, callback
from dash.exceptions import PreventUpdate
import interfaceUpdater

redisConector = rc.redisConector()

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

dash.register_page(__name__)
layout=html.Div(id='element-to-hide', style={'display':'none'}),\
        html.Div(
            children=[
            dcc.Interval(
                id='int-component-el',
                interval=225, # in milliseconds
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
                                children=html.Img(src="../assets/Balcon_ACCU.png", className="pedalbox-logo"),
                                className="grid1-1"
                            ),
                            html.Div(
                                children="ACCUMULATOR STATE",
                                className="grid25-1",
                                style={'text-align':'center'}
                            ),
                            html.Div(
                                children=[html.H5('AMS State Machine',
                                        style={'font-weight': 'bold','font-size':'16px'}
                                        ),
                                        html.H5('Waiting for data',
                                        id='smAMS3',
                                        style={'font-size':'26px'}
                                        ),
                                ],className="grid1-22"
                            ),
                            html.Div(                                        
                                children=[html.H5('AMS Error',
                                        style={'font-weight': 'bold','font-size':'16px'}
                                        ),
                                        html.H5('Waiting for data',
                                        id='errorAMS3',
                                        style={'font-size':'26px'}
                                        ),
                                ],
                                className="grid1-33"
                            ),
                            html.Div(
                                children=[html.H5('AMS Mode',
                                        style={'font-weight': 'bold','font-size':'16px'}
                                        ),
                                        html.H5('Waiting for data',
                                        id='modeAMS3',
                                        style={'font-size':'26px'}
                                        ),
                                ],
                                className="grid1-44"
                            ), 
                            html.Div(
                                children=[html.H5('Timed Out Slave',
                                        style={'font-weight': 'bold','font-size':'16px'}
                                        ),
                                        html.H5('Waiting for data',
                                        id='timedOutSlave3',
                                        style={'font-size':'26px', 'padding':'20%'}
                                        ),
                                ],
                                className="grid1-55"
                            ), 
                            html.Div(
                                children=daq.LEDDisplay(
                                        id='cellMinVoltage3',
                                        label={'label':"Cell min voltage", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                        labelPosition='top',
                                        value='3.64',
                                        color="black"
                                    ),
                                className="grid2-22"
                            ),
                            html.Div(
                                children=daq.LEDDisplay(
                                        id='cellMaxVoltage3',
                                        label={'label':"Cell max voltage", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                        labelPosition='top',
                                        value='0',
                                        color="black"

                                    ),
                                className="grid2-33"
                                ),
                            html.Div(
                                children=daq.Indicator(
                                            id='imd3',
                                            label={'label':"IMD", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                            color="red",
                                            size=45,
                                            value=True
                                        ),
                                className="grid2-44"
                            ),
                                html.Div(
                                children=daq.Indicator(
                                            id='k13',
                                            label={'label':"K1", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                            color="green",
                                            size=45,
                                            value=True
                                        ),
                                className="grid2-55"
                                ), 
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='idCellMinVoltage3',
                                            label={'label':"ID cell min voltage", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="grid3-22"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='idCellMaxVoltage3',
                                            label={'label':"ID cell max voltage", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="grid3-33"
                                ),
                                html.Div(
                                    children=daq.Indicator(
                                                id='k23',
                                                label={'label':"K2+", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                                color="green",
                                                size=45,
                                                value=True
                                            ),
                                    className="grid3-55"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='idCellMinVoltage3',
                                            label={'label':"ID cell min voltage", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="grid3-22"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='idCellMaxVoltage3',
                                            label={'label':"ID cell max voltage", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="grid3-33"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='cellMinTemp3',
                                            label={'label':"Cell Min Temp", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="grid4-22"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='cellMaxTemp3',
                                            label={'label':"Cell Max Temp", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="grid4-33"
                                ),
                                html.Div(
                                children=daq.Indicator(
                                            id='ams3',
                                            label={'label':"AMS", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                            color="red",
                                            size=45,
                                            value=True
                                        ),
                                className="grid4-44"
                                ),
                                html.Div(
                                    children=daq.Indicator(
                                                id='k33',
                                                label={'label':"K3-", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                                color="green",
                                                size=45,
                                                value=True
                                            ),
                                    className="grid4-55"
                                ), 
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='idCellMinTemp3',
                                            label={'label':"ID Cell Min Temp", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="grid5-22"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='idCellMaxTemp3',
                                            label={'label':"ID Cell Max Temp", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="grid5-33"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='totalVoltage3',
                                            label={'label':"Estimated Voltage", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="grid5-44"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='current3',
                                            label={'label':"Output Current", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="grid5-55"
                                ),
                        ],
                        className="cornerWrapperMulti"
                    )
                ],
                className="box"
            ),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children=html.Img(src="../assets/Balcon_ACCU.png", className="pedalbox-logo"),
                                className="grid1-1"
                            ),
                            html.Div(
                                children="MOTORS & INVERTERS",
                                className="grid25-1",
                                style={'text-align':'center'}
                            ),
                            html.Div(
                                children=[daq.Gauge(
                                    id='SpeedFL2',
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
                                ],className="grid1-22"
                            ),
                            html.Div(                                        
                                children=[daq.Gauge(
                                    id='SpeedRL2',
                                    style={'width': '100%', 'height':'100%', 'margin':{'l':'0','r':'0','b':'0','t':'0'}},
                                    size=160,
                                    label={'label':"Speed RL", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                    color="#e30202",
                                    scale={'start': 0, 'interval': 1000, 'labelInterval': 4},
                                    showCurrentValue=True,
                                    units="RPM",
                                    value=5000,
                                    min=0,
                                    max=20000,
                                    ),
                                ],
                                className="grid1-33"
                            ),
                            html.Div(
                                children=[html.H5('AMS Mode',
                                        style={'font-weight': 'bold','font-size':'16px'}
                                        ),
                                        html.H5('Waiting for data',
                                        id='modeAMS3',
                                        style={'font-size':'26px'}
                                        ),
                                ],
                                className="grid1-44"
                            ), 
                            html.Div(
                                children=[html.H5('Timed Out Slave',
                                        style={'font-weight': 'bold','font-size':'16px'}
                                        ),
                                        html.H5('Waiting for data',
                                        id='timedOutSlave3',
                                        style={'font-size':'26px', 'padding':'20%'}
                                        ),
                                ],
                                className="grid1-55"
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
                                    value=5000,
                                    min=0,
                                    max=20000,
                                    ),
                                className="grid2-22"
                            ),
                            html.Div(
                                children=daq.Gauge(
                                    id='SpeedRR',
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
                                className="grid2-33"
                                ),
                            html.Div(
                                children=daq.Indicator(
                                            id='imd3',
                                            label={'label':"IMD", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                            color="red",
                                            size=45,
                                            value=True
                                        ),
                                className="grid2-44"
                            ),
                                html.Div(
                                children=daq.Indicator(
                                            id='k13',
                                            label={'label':"K1", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                            color="green",
                                            size=45,
                                            value=True
                                        ),
                                className="grid2-55"
                                ), 
                                html.Div(
                                    children=daq.Thermometer(
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
                                    className="grid3-22"
                                ),
                                html.Div(
                                    children=daq.Thermometer(
                                                    id='tempRL',
                                                    value=40,
                                                    height=110,
                                                    min=0,
                                                    max=80,
                                                    showCurrentValue=True,
                                                    style={
                                                        'margin-left': '-80px', 'margin-bottom' : '20px', 'margin-top' : '-40px'
                                                    }
                                                ),
                                    className="grid3-33"
                                ),
                                html.Div(
                                    children=daq.Thermometer(
                                                    id='tempFR',
                                                    value=40,
                                                    height=110,
                                                    min=0,
                                                    max=80,
                                                    showCurrentValue=True,
                                                    style={
                                                        'margin-left': '-80px', 'margin-bottom' : '20px', 'margin-top' : '-40px'
                                                    }
                                                ),
                                    className="grid3-44"
                                ),
                                html.Div(
                                    children=daq.Thermometer(
                                                    id='tempRR',
                                                    value=40,
                                                    height=110,
                                                    min=0,
                                                    max=80,
                                                    showCurrentValue=True,
                                                    style={
                                                        'margin-left': '-80px', 'margin-bottom' : '20px', 'margin-top' : '-40px'
                                                    }
                                                ),
                                    className="grid3-55"
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
                                    className="grid4-22"
                                ),
                                html.Div(
                                    children=daq.Gauge(
                                    id='powerRL',
                                    style={'width': '100%', 'height':'100%', 'margin':{'l':'0','r':'0','b':'0','t':'0'}},
                                    size=160,
                                    label={'label':"Power RL", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                    color="#e30202",
                                    showCurrentValue=True,
                                    units="W",
                                    value=0,
                                    min=-524288,
                                    max=524272,
                                    ),
                                    className="grid4-33"
                                ),
                                html.Div(
                                children=dcc.Graph(
                                        id="powers",
                                        figure={'layout':{"autosize":False}},
                                        style={'width': '100%', 'height':'100%', 'margin':{'l':'-500px','r':'0','b':'0','t':'0'}},
                                        config={"responsive":True,"displayModeBar": False, "edits":{"titleText":False,"legendText":False, "annotationPosition":False,"colorbarTitleText":False},"displayModeBar":True},

                                    ),
                                className="grid45-45"
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
                                    className="grid5-22"
                                ),
                                html.Div(
                                    children=daq.Gauge(
                                    id='powerRR',
                                    style={'width': '100%', 'height':'100%', 'margin':{'l':'0','r':'0','b':'0','t':'0'}},
                                    size=160,
                                    label={'label':"Power RR", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                    color="#e30202",
                                    showCurrentValue=True,
                                    units="W",
                                    value=0,
                                    min=-524288,
                                    max=524272,
                                    ),
                                    className="grid5-33"
                                ),
                        ],
                        className="cornerWrapperMulti"
                    )
                ],
                className="box"
            ),
            html.Div(
                    children=[
                            html.Div(
                                children=[
                                html.Div(children=[
                                    html.Div(children=[
                                        daq.Indicator(
                                                id="motor1",
                                                label=latchedStatus[status],
                                                labelPosition="right",
                                                color="grey",
                                                value=False,
                                                style={'float' : 'left', 'margin-right':'18%'}
                                                )for status in latchedStatus
                                    ], className="motor1"),
                                    html.Div(children=[daq.Indicator(
                                                id="motor2",
                                                label=latchedStatus[status],
                                                labelPosition="right",
                                                color="grey",
                                                value=False,
                                                style={'float' : 'left', 'margin-right':'18%'}
                                                )for status in latchedStatus
                                    ], className="motor2"),
                                    html.Div(children=[daq.Indicator(
                                                id="motor3",
                                                label=latchedStatus[status],
                                                labelPosition="right",
                                                color="grey",
                                                value=False,
                                                style={'float' : 'left', 'margin-right':'18%'},
                                                )for status in latchedStatus
                                    ], className="motor3"),
                                    html.Div(children=[daq.Indicator(
                                                id="motor4",
                                                label=latchedStatus[status],
                                                labelPosition="right",
                                                color="grey",
                                                value=False,
                                                style={'float' : 'left', 'margin-right':'18%'}
                                                )for status in latchedStatus
                                    ], className="motor4")],
                                className="contenedorMotores"
                                )
                                ], 
                            )                     
                    ],
                    className="box"
                ),
        ],
    className='container4'
    )

@callback(
    [Output('smAMS3', 'children'), Output('errorAMS3', 'children'), Output('modeAMS3', 'children'), Output('timedOutSlave3', 'children'), Output('cellMinVoltage3', 'value'), Output('cellMaxVoltage3', 'value'), Output('idCellMaxVoltage3', 'value'), Output('idCellMinVoltage3', 'value'), Output('cellMinTemp3', 'value'), Output('cellMaxTemp3', 'value'), Output('idCellMinTemp3', 'value'), Output('idCellMaxTemp3', 'value'), Output('totalVoltage3', 'value'), Output('current3', 'value'), Output('k13', 'color'), Output('k23', 'color'), Output('k33', 'color'), Output('cellMinVoltage3', 'color'), Output('cellMaxTemp3', 'color'), Output('imd3', 'color'), Output('ams3', 'color'), Output('powers', 'figure')],
    Input('int-component-el', 'n_intervals'),
)
def acutaliza(N):
    #begining = time.time()
    #data = get_data()
    #vel = random.randint(0,10)
    pedalera = interfaceUpdater.updatePedaleraMulti(redisConector.get_value('0001'))
    #end = time.time()
    #print(end-begining)

    ###MASTER###
    totalVoltage, minVoltage, idMinVoltage, voltageColor, maxVoltage, idMaxVoltage, minTemp, idMinTemp, maxTemp, idMaxTemp, colorTemp = interfaceUpdater.updateVoltages(redisConector.get_value('0311'))
    k1, k2, k3, smAMS, errorAMS, imd, amsMode, timedOutSlvave, current, amsLed = interfaceUpdater.contactorFeedbackAndAMSState(redisConector.get_value('0310'))

    ##INVERTERS&MOTORS##
    speedFL, speedFR, speedRL, speedRR = interfaceUpdater.motorRPM(redisConector.get_value('024f'), redisConector.get_value('034f'), redisConector.get_value('024e'), redisConector.get_value('034e'))
    tempFL, tempFR, tempRL, tempRR, powerFL, powerFR, powerRL, powerRR = interfaceUpdater.powerAndDCVoltage(redisConector.get_value('028f'), redisConector.get_value('038f'), redisConector.get_value('028e'), redisConector.get_value('038e'))
    powerFigure = interfaceUpdater.powerFigure(redisConector.get_value('028f'), redisConector.get_value('038f'), redisConector.get_value('028e'), redisConector.get_value('038e'))



    return smAMS, errorAMS, amsMode, timedOutSlvave, minVoltage, maxVoltage, idMaxVoltage, idMinVoltage, minTemp, maxTemp, idMinTemp, idMaxTemp, totalVoltage, current, k1, k2, k3, voltageColor, colorTemp, imd, amsLed, powerFigure

import random
from JSONReader import get_0001, get_data
import dash
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash import html, Dash, Input, ctx, Output, dcc, callback
from dash.exceptions import PreventUpdate
import interfaceUpdater
import redisConector as rc

redisConector = rc.redisConector()
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
                                children=html.Img(src="../assets/ecu.png", className="pedalbox-logo"),
                                className="grid1-1"
                            ),
                            html.Div(
                                children="ECU",
                                className="grid25-1",
                                style={'text-align':'center'}
                            ),
                            html.Div(
                                children=[html.H5('Car State',
                                        style={'font-weight': 'bold','font-size':'16px'}
                                        ),
                                        html.H5('Waiting for data',
                                        id='carState2',
                                        style={'font-size':'26px'}
                                        ),
                                ],className="grid1-22"
                            ),
                            html.Div(                                        
                                children=[html.H5('Error',
                                        style={'font-weight': 'bold','font-size':'16px'}
                                        ),
                                        html.H5('Waiting for data',
                                        id='error2',
                                        style={'font-size':'26px'}
                                        ),
                                ],
                                className="grid1-33"
                            ),
                            html.Div(
                                children=[html.H5('Safety',
                                        style={'font-weight': 'bold','font-size':'16px'}
                                        ),
                                        html.H5('Waiting for data',
                                        id='error2',
                                        style={'font-size':'26px'}
                                        ),
                                ],
                                className="grid2-22"
                            ),
                            html.Div(
                                children=[html.H5('Safety Front',
                                        style={'font-weight': 'bold','font-size':'16px'}
                                        ),
                                        html.H5('Waiting for data',
                                        id='error2',
                                        style={'font-size':'26px'}
                                        ),
                                ],
                                className="grid2-33"
                                ),
                            html.Div(
                                children=daq.Indicator(
                                            id='Plausibility',
                                            label={'label':"Plausibility", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                            color="yellow",
                                            size=45,
                                            value=True
                                        ),
                                className="box7"
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
                                className="box10"
                            ),
                            html.Div(
                                children=daq.LEDDisplay(
                                        id='vel',
                                        label={'label':"Speed", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                        labelPosition='top',
                                        value='0',
                                        color="black"
                                    ),
                                className="box11"
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
                                children="AMS",
                                className="grid25-1",
                                style={'text-align':'center'}
                            ),
                            html.Div(
                                children=[html.H5('AMS State Machine',
                                        style={'font-weight': 'bold','font-size':'16px'}
                                        ),
                                        html.H5('Waiting for data',
                                        id='smAMS2',
                                        style={'font-size':'26px'}
                                        ),
                                ],className="grid1-22"
                            ),
                            html.Div(                                        
                                children=[html.H5('AMS Error',
                                        style={'font-weight': 'bold','font-size':'16px'}
                                        ),
                                        html.H5('Waiting for data',
                                        id='errorAMS2',
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
                                        id='modeAMS2',
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
                                        id='timedOutSlave2',
                                        style={'font-size':'26px'}
                                        ),
                                ],
                                className="grid1-55"
                            ), 
                            html.Div(
                                children=daq.LEDDisplay(
                                        id='cellMinVoltage2',
                                        label={'label':"Cell min voltage", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                        labelPosition='top',
                                        value='3.64',
                                        color="black"
                                    ),
                                className="grid2-22"
                            ),
                            html.Div(
                                children=daq.LEDDisplay(
                                        id='cellMaxVoltage2',
                                        label={'label':"Cell max voltage", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                        labelPosition='top',
                                        value='0',
                                        color="black"

                                    ),
                                className="grid2-33"
                                ),
                            html.Div(
                                children=daq.Indicator(
                                            id='imd2',
                                            label={'label':"IMD", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                            color="red",
                                            size=45,
                                            value=True
                                        ),
                                className="grid2-44"
                            ),
                                html.Div(
                                children=daq.Indicator(
                                            id='k12',
                                            label={'label':"K1", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                            color="green",
                                            size=45,
                                            value=True
                                        ),
                                className="grid2-55"
                                ), 
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='idCellMinVoltage2',
                                            label={'label':"ID cell min voltage", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="grid3-22"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='idCellMaxVoltage2',
                                            label={'label':"ID cell max voltage", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="grid3-33"
                                ),
                                html.Div(
                                    children=daq.Indicator(
                                                id='k22',
                                                label={'label':"K2+", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                                color="green",
                                                size=45,
                                                value=True
                                            ),
                                    className="grid3-55"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='idCellMinVoltage2',
                                            label={'label':"ID cell min voltage", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="grid3-22"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='idCellMaxVoltage2',
                                            label={'label':"ID cell max voltage", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="grid3-33"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='cellMinTemp2',
                                            label={'label':"Cell Min Temp", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="grid4-22"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='cellMaxTemp2',
                                            label={'label':"Cell Max Temp", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="grid4-33"
                                ),
                                html.Div(
                                    children=daq.Indicator(
                                                id='ams2',
                                                label={'label':"AMS", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                                color="red",
                                                size=45,
                                                value=True
                                            ),
                                    className="grid4-44"
                                ),
                                html.Div(
                                    children=daq.Indicator(
                                                id='k32',
                                                label={'label':"K3-", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                                color="green",
                                                size=45,
                                                value=True
                                            ),
                                    className="grid4-55"
                                ), 
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='idCellMinTemp2',
                                            label={'label':"ID Cell Min Temp", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="grid5-22"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='idCellMaxTemp2',
                                            label={'label':"ID Cell Max Temp", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="grid5-33"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='totalVoltage2',
                                            label={'label':"Estimated Voltage", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"
                                        ),
                                    className="grid5-44"
                                ),
                                html.Div(
                                    children=daq.LEDDisplay(
                                            id='current2',
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
                                children=html.Img(src="../assets/dash.jpeg", className="pedalbox-logo"),
                                className="grid1-1"
                            ),
                            html.Div(
                                children="Dash",
                                className="grid25-1"
                            ),
                            html.Div(
                                children=[html.H5('State Machine State',
                                        style={'font-weight': 'bold','font-size':'16px'}
                                        ),
                                        html.H5('Waiting for data',
                                        id='dashSM',
                                        style={'font-size':'26px'}
                                        ),
                                ],className="grid1-22"
                            ),
                            html.Div(                                        
                                children=[html.H5('Previous State',
                                        style={'font-weight': 'bold','font-size':'16px'}
                                        ),
                                        html.H5('Waiting for data',
                                        id='dashPrevSM',
                                        style={'font-size':'26px'}
                                        ),
                                ],
                                className="grid1-33"
                            ),
                            html.Div(
                                children=[html.H5('Safe OK',
                                        style={'font-weight': 'bold','font-size':'16px'}
                                        ),
                                        html.H5('Waiting for data',
                                        id='error2',
                                        style={'font-size':'26px'}
                                        ),
                                ],
                                className="grid2-22"
                            ),
                            html.Div(
                                children=[html.H5('Safety Front',
                                        style={'font-weight': 'bold','font-size':'16px'}
                                        ),
                                        html.H5('Waiting for data',
                                        id='safetyFront2',
                                        style={'font-size':'26px'}
                                        ),
                                ],
                                className="grid2-33"
                                ),
                            html.Div(
                                children=daq.LEDDisplay(
                                            id='power2',
                                            label={'label':"POWER", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"

                                        ),
                                className="grid3-22"
                            ),
                            html.Div(
                                children=daq.LEDDisplay(
                                            id='tv',
                                            label={'label':"TV VALUE", 'style':{'font-weight': 'bold','font-size':'16px'}},
                                            labelPosition='top',
                                            value='0',
                                            color="black"

                                        ),
                                className="grid3-33"
                            ),
                            html.Div(
                                children=daq.Indicator(
                                            id='loadon',
                                            label={'label':"LOAD ON", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                            color="green",
                                            size=45,
                                            value=True
                                        ),
                                className="grid1-44"
                            ), 
                            html.Div(
                                children=daq.Indicator(
                                            id='start',
                                            label={'label':"START", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                            color="green",
                                            size=45,
                                            value=True
                                        ),
                                className="grid1-55"
                            ), 
                            html.Div(
                                children=daq.Indicator(
                                            id='PW+',
                                            label={'label':"PW+", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                            color="green",
                                            size=45,
                                            value=True
                                        ),
                                className="grid2-44"
                            ), 
                            html.Div(
                                children=daq.Indicator(
                                            id='PW-',
                                            label={'label':"PW-", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                            color="green",
                                            size=45,
                                            value=True
                                        ),
                                className="grid2-55"
                            ), 
                            html.Div(
                                children=daq.Indicator(
                                            id='TV+',
                                            label={'label':"TV+", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                            color="green",
                                            size=45,
                                            value=True
                                        ),
                                className="grid3-44"
                            ), 
                            html.Div(
                                children=daq.Indicator(
                                            id='TV-',
                                            label={'label':"TV-", 'style':{'font-weight': 'bold','font-size':'20px'}},
                                            color="green",
                                            size=45,
                                            value=True
                                        ),
                                className="grid3-55"
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
                                    children=html.Img(src="../assets/PedalBox.jpg", className="pedalbox-logo"),
                                    className="box1"
                                ),
                                html.Div(
                                    children="Pedalera",
                                    className="box2"
                                ),
                                html.Div(
                                    children=[dcc.Graph(
                                        id="pedalera",
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
        ],
    className='container3'
    )

@callback(
    [Output("pedalera", "figure"), Output('smAMS2', 'children'), Output('errorAMS2', 'children'), Output('modeAMS2', 'children'), Output('timedOutSlave2', 'children'), Output('cellMinVoltage2', 'value'), Output('cellMaxVoltage2', 'value'), Output('idCellMaxVoltage2', 'value'), Output('idCellMinVoltage2', 'value'), Output('cellMinTemp2', 'value'), Output('cellMaxTemp2', 'value'), Output('idCellMinTemp2', 'value'), Output('idCellMaxTemp2', 'value'), Output('totalVoltage2', 'value'), Output('current2', 'value'), Output('k12', 'color'), Output('k22', 'color'), Output('k32', 'color'), Output('cellMinVoltage2', 'color'), Output('cellMaxTemp2', 'color'), Output('imd2', 'color'), Output('ams2', 'color'), Output('dashSM', 'children'), Output('dashPrevSM', 'children'), Output('loadon', 'color'), Output('start', 'color'), Output('PW+', 'color'), Output('TV+', 'color'), Output('PW-', 'color'),Output('TV-', 'color'), Output('power2', 'value'), Output('tv', 'value'), Output('safetyFront2', 'children')],
    Input('int-component-el', 'n_intervals'),
)
def acutaliza(N):
    ##PEDALERA##
    pedalera = interfaceUpdater.updatePedaleraMulti(redisConector.get_value('0001'))
    ###MASTER###
    totalVoltage, minVoltage, idMinVoltage, voltageColor, maxVoltage, idMaxVoltage, minTemp, idMinTemp, maxTemp, idMaxTemp, colorTemp = interfaceUpdater.updateVoltages(redisConector.get_value('0311'))
    k1, k2, k3, smAMS, errorAMS, imd, amsMode, timedOutSlvave, current, amsLed = interfaceUpdater.contactorFeedbackAndAMSState(redisConector.get_value('0310'))
    
    ##DASH##
    safetyFront = interfaceUpdater.safetyFront(redisConector.get_value('00a2'))
    loadON, start, powerPlus, tvPlus, powerMinus, tvMinus, state, prevState = interfaceUpdater.dashData2(redisConector.get_value('00a2'))
    power, torqueValue = interfaceUpdater.dashData(redisConector.get_value('00a2'))
    return pedalera, smAMS, errorAMS, amsMode, timedOutSlvave, minVoltage, maxVoltage, idMaxVoltage, idMinVoltage, minTemp, maxTemp, idMinTemp, idMaxTemp, totalVoltage, current, k1, k2, k3, voltageColor, colorTemp, imd, amsLed, state, prevState, loadON, start, powerPlus, tvPlus, powerMinus, tvMinus, power, torqueValue, safetyFront

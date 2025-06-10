import re
import dash
from dash import Dash, html, Input, Output, dcc, ctx, callback
import dash_daq as daq
import pandas as pd
import os
import figureCreator

dash.register_page(__name__)

dataDict = {}
regexWheel = re.compile('^Wheel_1')
length = 0
lengthMax = 0
for log in os.listdir("logs"):
    dataDict[log] = pd.read_excel("logs/"+log)
    dataDict[log].columns = ['Time', 'Posicion_X_CG', 'Posicion_Y_CG', 'Posicion_Z_CG', 'Velocidad_X_CG', 'Velocidad_Y_CG', 'Velocidad_Z_CG', 'Aceleracion_X_CG', 'Aceleracion_Y_CG', 'Aceleracion_Z_CG', 'Roll_euler', 'Pitch_euler', 'Yaw_euler', 'Roll_rate', 'Pitch_rate', 'Yaw_rate', 'Roll_accel', 'Pitch_accel', 'Yaw_accel', 'Slip_angle_chassis', 'Total_speed_chassis', 'Longitudinal_speed_ch_kmh', 'Torque_vect_status', 'Torque_vect_button', 'Normalizad_steering_wheel_angle', 'Torque_steering_wheel', "Wheel_1_Fx", "Wheel_1_Fy", "Wheel_1_Fz", "Wheel_1_Mx", "Wheel_1_My_torque", "Wheel_1_Mz", "Wheel_1_Spin_Accel", "Wheel_1_Spin_Rate", "Wheel_2_Fx", "Wheel_2_Fy", "Wheel_2_Fz", "Wheel_2_Mx", "Wheel_2_My_torque", "Wheel_2_Mz", "Wheel_2_Spin_Accel", "Wheel_2_Spin_Rate", "Wheel_3_Fx", "Wheel_3_Fy", "Wheel_3_Fz", "Wheel_3_Mx", "Wheel_3_My_torque", "Wheel_3_Mz", "Wheel_3_Spin_Accel", "Wheel_3_Spin_Rate", "Wheel_4_Fx", "Wheel_4_Fy", "Wheel_4_Fz", "Wheel_4_Mx", "Wheel_4_My_torque", "Wheel_4_Mz", "Wheel_4_Spin_Accel", "Wheel_4_Spin_Rate"]
    dataDict[log].sort_values("Time", inplace=True)
    length = len(dataDict[log])
    if(length>lengthMax):
        lengthMax = length
        idLength = log



layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Img(src="../assets/fsb_round_logo.png", className="header-logo"),
                html.H1(
                    children="Dynacar Log Reader", className="header-title"
                ),
                html.P(
                    children="Analyze Tecnalia's Dynacar log outputs for Formula Student Bizkaia's Torque Vectoring division.",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(children="Log", className="menu-title"),
                            dcc.Dropdown(
                                id="log-filter",
                                options=[
                                    {"label": log, "value": log}
                                    for log in os.listdir("logs")
                                ],
                                value="CarData.xlsx",
                                clearable=False,
                                className="dropdown",
                                multi=False,
                            ),
                        ],
                        className="option"
                    ),
                    html.Div(
                        children=[
                            html.Div(children="Value", className="menu-title"),
                            dcc.Dropdown(
                                id="data-filter",
                                options=[
                                    {"label": dato, "value": dato}
                                    for dato in list(dataDict.values())[0].columns
                                ],
                                value="Total_speed_chassis",
                                clearable=False,
                                searchable=False,
                                className="dropdown",
                            ),
                        ],
                        className="option"
                    ),
                ],
                className="subMenu"
            ),
            html.Br(),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children="Time interval", className="menu-title"
                            ),
                            dcc.RangeSlider(
                                id="time-range",
                                min=dataDict[idLength].Time.min(),
                                max=dataDict[idLength].Time.max(),
                                value=[dataDict[idLength].Time.min(), dataDict[idLength].Time.max()],
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                            html.Div(
                                children="Comparisons", className="menu-title"
                            ),
                            daq.PowerButton(
                            id='comparisons',
                            on=False,
                            color='#FF5E5E'
                        ),
                        ]
                    ),
                ],
                className="subMenu"
            ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False, "edits":{"legendText":True, "annotationPosition":True},"displayModeBar":True},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Wheel data", className="menu-title")
                    ],
                    className="subMenu"
                ),
                dcc.Dropdown(
                    id="corner-filter",
                    options=[
                        {"label": dato.split("1_", 1)[1], "value": dato.split("1_", 1)[1]}
                        for dato in list(dataDict.values())[0].columns if regexWheel.match(dato)
                    ],
                    value="My_torque",
                    clearable=False,
                    searchable=False,
                    className="dropdown",
                ),
            ],
            className="menu"
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    children=html.Img(src="../assets/corner.png", className="corner-logo"),
                                    className="box1"
                                ),
                                html.Div(
                                    children="Corner 1",
                                    className="box2"
                                ),
                                html.Div(
                                    children=dcc.Graph(
                                        id="corner1-chart",
                                        config={"displayModeBar": False,
                                                "edits": {"legendText": False, "annotationPosition": True, "titleText" : False},
                                                },
                                        figure={"layout": {
                                                "height": 300,  # px
                                                "frameMargins": 0
                                        }
                                        },
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
                                    children=html.Img(src="../assets/corner.png", className="corner-logo"),
                                    className="box1"
                                ),
                                html.Div(
                                    children="Corner 2",
                                    className="box2"
                                ),
                                html.Div(
                                    children=dcc.Graph(
                                        id="corner2-chart",
                                        config={"displayModeBar": False,
                                                "edits": {"legendText": False, "annotationPosition": True,
                                                          "titleText": False},
                                                },
                                        figure={"layout": {
                                            "height": 300,  # px
                                            "frameMargins": 0
                                        }
                                        },
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
                                    children=html.Img(src="../assets/corner.png", className="corner-logo"),
                                    className="box1"
                                ),
                                html.Div(
                                    children="Corner 3",
                                    className="box2"
                                ),
                                html.Div(
                                    children=dcc.Graph(
                                        id="corner3-chart",
                                        config={"displayModeBar": False,
                                                "edits": {"legendText": False, "annotationPosition": True,
                                                          "titleText": False},
                                                },
                                        figure={"layout": {
                                            "height": 300,  # px
                                            "frameMargins": 0
                                        }
                                        },
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
                                    children=html.Img(src="../assets/corner.png", className="corner-logo"),
                                    className="box1"
                                ),
                                html.Div(
                                    children="Corner 4",
                                    className="box2"
                                ),
                                html.Div(
                                    children=dcc.Graph(
                                        id="corner4-chart",
                                        config={"displayModeBar": False,
                                                "edits": {"legendText": False, "annotationPosition": True,
                                                          "titleText": False},
                                                },
                                        figure={"layout": {
                                            "height": 300,  # px
                                            "frameMargins": 0
                                        }
                                        },
                                    ),
                                    className="box3"
                                ),
                                dcc.Interval(
                                            id='interval-component',
                                            interval=1*1000, # in milliseconds
                                            n_intervals=0
                                        ),
                            ],
                            className="cornerWrapper"
                        )
                    ],
                    className="box"
                )
            ],
            className="container"
        ),
        html.Br(),
        html.Div(
            children=[
                html.Div(
                    children=daq.Gauge(
                            label='Torque',
                            color="#e30202",
                            scale={'start': 0, 'interval': 2, 'labelInterval': 2},
                            showCurrentValue=True,
                            units="Nm",
                            value=3,
                            min=0,
                            max=21.9,
                            ),
                    className="boxLive"
                ),
                html.Div(
                    children=daq.Gauge(
                            label='Torque',
                            color="#e30202",
                            scale={'start': 0, 'interval': 2, 'labelInterval': 2},
                            showCurrentValue=True,
                            units="Nm",
                            value=3,
                            min=0,
                            max=21.9,
                            ),
                    className="boxLive"
                ),
                html.Div(
                    children=daq.Gauge(
                        label='Torque',
                        color="#e30202",
                        scale={'start': 0, 'interval': 2, 'labelInterval': 2},
                        showCurrentValue=True,
                        units="Nm",
                        value=3,
                        min=0,
                        max=21.9,
                    ),
                    className="boxLive"
                ),
                html.Div(
                    children=daq.Gauge(
                        label='Torque',
                        color="#e30202",
                        scale={'start': 0, 'interval': 2, 'labelInterval': 2},
                        showCurrentValue=True,
                        units="Nm",
                        value=3,
                        min=0,
                        max=21.9,
                    ),
                    className="boxLive"
                ),
            ],
            className="container"
        ),
        html.Div(
            children=[
                daq.Gauge(
                label='Torque',
                color="#e30202",
                scale={'start': 0, 'interval': 2, 'labelInterval': 2},
                showCurrentValue=True,
                units="Nm",
                value=3,
                min=0,
                max=21.9,
                ),
                daq.Gauge(
                label='Scale',
                color="#e30202",
                scale={'start': 0, 'interval': 3, 'labelInterval': 2},
                showCurrentValue=True,
                units="Nm",
                value=3,
                min=0,
                max=21.9,
                ),
            ],
            className="menuRueda",
        ),
    ],
    className="body"
)

#########CALLBACKS################
@callback(
    [Output("price-chart", "figure"), Output("log-filter", "multi"), Output("corner1-chart", "figure"), Output("corner2-chart", "figure"), Output("corner3-chart", "figure"), Output("corner4-chart", "figure") ],
    [
        Input("comparisons", "on"),
        Input("log-filter", "value"),
        Input("data-filter", "value"),
        Input("time-range", "value"),
        Input("corner-filter", "value"),
    ],
)
def update_charts(on, log, dato, value, datoCorner):
    print("ALO")
    figure_1, multi = figureCreator.createFigure1(dataDict, on, log, dato, value, ctx.triggered_id == 'comparisons')
    corner_1 = figureCreator.createFigure2(dataDict, on, log, datoCorner, value, ctx.triggered_id == 'comparisons', 1)
    corner_2 = figureCreator.createFigure2(dataDict, on, log, datoCorner, value, ctx.triggered_id == 'comparisons', 2)
    corner_3 = figureCreator.createFigure2(dataDict, on, log, datoCorner, value, ctx.triggered_id == 'comparisons', 3)
    corner_4 = figureCreator.createFigure2(dataDict, on, log, datoCorner, value, ctx.triggered_id == 'comparisons', 4)

    return figure_1, multi, corner_1, corner_2, corner_3, corner_4

import dash.html as html
import dash_daq as daq
import plotly.graph_objects as go

statuses = [
    "Event buffer has a new event entry since last upload",
    "Event buffer is full and has missed at least one event",
    "Power module over current detected by hardware",
    "Power module current offset calibration failed",
    "Power module temperature sensor defective",
    "Power module temperature has reached warning level",
    "Power module temperature has reached error level",
    "Power module i*t error",
    "Power module over current detected by software",
    "Power module pattern data inconsistency",
    "Dc link over voltage detected by hardware",
    "Dc link over voltage detected by software",
    "Dc link undervoltage detectedy by software",
    "Fault of the other inverter on the same device",
    "Motor temperature sensor defective",
    "Motor temperature has reached warning level",
    "Motor temperature has reached error level",
    "Motor stator frequency to high",
    "Board supply voltage error",
    "Receive PDO timeout",
    "NMT not in state operational",
    "Task calculation time overrun",
    "Net synchronisation error",
    "Position device signal to low",
    "Position device signal to high",
    "Resolver calibration failed",
    "System error, analog input or motor feedback DMA error",
    "Interlock open due to open cover sheet",
    "Gate driver disabled by APPC",
    "Motor stall error",
    "Ambient temperature has reached warning level",
    "Ambient temperature has reached error level"
]


STATES = {'00' : 'Safe 1',
    '02' : 'Safe 2 FRONT',
    '08' : 'Safe 3 Mainhoop',
    '09' : 'Safe 4 Accu',
    '0a' : 'Safe 5 RL',
    '0b' : 'Safe 6 RR',
    '0c' : 'Safe 7 BSPD',
    '0d' : 'Safe 8 Interlocks',
    '0e' : 'Safe End Vload',
    '0f' : 'Safe OK'
}

CARSTATES = {
    '00' : 'Init',
    '01' : 'Standby',
    '02' : 'Precharge',
    '03' : 'Energized',
    '04' : 'Running',
    '05' : 'Denergized',
    '06' : 'Error'
}

AMSSTATES = {
    '01' : 'Charge waiting',
    '02' : 'Charge precharge',
    '03' : 'Charge charging',
    '04' : 'Car waiting',
    '05' : 'Car precharge',
    '06' : 'Car RTD',
    '07' : 'Error',
    '08' : 'Critical Error'
}

AMSERRORS = {
    '0' : 'OK',
    '1' : 'VLoad',
    '2' : 'Current',
    '4' : 'IMD',
    '8' : 'Contactors',
    '16' : 'Voltaje',
    '32' : 'Temperature',
    '64' : 'ECU Timeout',
    '128' : 'Slaves Timeout'
}

PilaPedalera =['0000000000000000' for i in range(50)]
PilaId0310 =['0000000000000000' for i in range(50)]
PilaCurrentFL = ['0000000000000000' for i in range(50)]
PilaCurrentFR = ['0000000000000000' for i in range(50)]
PilaCurrentRL = ['0000000000000000' for i in range(50)]
PilaCurrentRR = ['0000000000000000' for i in range(50)]
PilaYawRate = ['0000000000000000' for i in range(50)]
PilaYawRateRef = ['0000000000000000' for i in range(50)]
PilaPowerFL = ['0000000000000000' for i in range(50)]
PilaPowerFR = ['0000000000000000' for i in range(50)]
PilaPowerRL = ['0000000000000000' for i in range(50)]
PilaPowerRR = ['0000000000000000' for i in range(50)]

def updateFigure1(data):
    PilaPedalera.pop(0)
    PilaPedalera.insert(49, data)
    datosAcc = [int(i[0:2],base=16) for i in PilaPedalera]
    datosBrk = [int(i[6:8],base=16) for i in PilaPedalera]
    datosX = [i for i in range(len(datosAcc))]
    figure_1 = go.Figure(

        data = [go.Scatter(
            x = datosX,
            y = datosAcc,
            mode = 'lines',
            name='Acc',
            marker = dict(color = 'green')
        ),
            go.Scatter(
                x=datosX,
                y=datosBrk,
                mode='lines',
                name='Brk',
                marker=dict(color='red')
            ),
        ]
    )
    figure_1['layout']['yaxis'] = {'range': (0, 250)}
    return figure_1

def updatePedaleraMulti(data):
    PilaPedalera.pop(0)
    PilaPedalera.insert(49, data)
    datosAcc1 = [int(i[0:2],base=16) for i in PilaPedalera]
    datosAcc2 = [int(i[2:4],base=16) for i in PilaPedalera]
    datosAcc3 = [int(i[4:6],base=16) for i in PilaPedalera]
    datosBrk = [int(i[6:8],base=16) for i in PilaPedalera]
    datosX = [i for i in range(len(datosAcc1))]
    figure_1 = go.Figure(

        data = [go.Scatter(
            x = datosX,
            y = datosAcc1,
            mode = 'lines',
            name='Acc1',
            marker = dict(color = 'green')
        ),
            go.Scatter(
                x=datosX,
                y=datosBrk,
                mode='lines',
                name='Brk',
                marker=dict(color='red')
            ),
            go.Scatter(
                x=datosX,
                y=datosAcc2,
                mode='lines',
                name='Acc2',
                marker=dict(color='blue')
            ),
            go.Scatter(
                x=datosX,
                y=datosAcc3,
                mode='lines',
                name='Acc3',
                marker=dict(color='purple')
            ),
        ]
    )
    figure_1['layout']['yaxis'] = {'range': (0, 255)}
    return figure_1




def updateFigure2(data):
    datosY = []
    datosY.append(int(data[0:2], base=16))
    datosY.append(int(data[3:5], base=16))
    datosX = [i for i in range(len(datosY))]

    figure_2 = {
        "data": [
            {
                "x": datosX,
                "y": datosY,
                "type": "lines",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "xaxis": {"fixedrange": True},
            "yaxis": {"range":(0,200)},
            "colorway": ["#e30202", "#302f2f", "#000000", "#15ff00", "#0062ff", "#ff00f7"],
        },
    }
    return figure_2



def currents(data1, data2, data3, data4):
    PilaCurrentFL.pop(0)
    PilaCurrentFL.insert(49, data1)
    PilaCurrentFR.pop(0)
    PilaCurrentFR.insert(49, data2)
    PilaCurrentRL.pop(0)
    PilaCurrentRL.insert(49, data3)
    PilaCurrentRR.pop(0)
    PilaCurrentRR.insert(49, data4)
    current1 = [int(i[12:14] + i[14:16], base=16) for i in PilaCurrentFL]
    current2 = [int(i[12:14] + i[14:16], base=16) for i in PilaCurrentFR]
    current3 = [int(i[12:14] + i[14:16], base=16) for i in PilaCurrentRL]
    current4 = [int(i[12:14] + i[14:16], base=16) for i in PilaCurrentRR]
    datosX = [i for i in range(len(current1))]
    figure_1 = go.Figure(
        data=[go.Scatter(
            x=datosX,
            y=current1,
            mode='lines',
            name='Current FL',
            marker=dict(color='green')
        ),
            go.Scatter(
                x=datosX,
                y=current2,
                mode='lines',
                name='Current FR',
                marker=dict(color='red')
            ),
            go.Scatter(
                x=datosX,
                y=current3,
                mode='lines',
                name='Current RL',
                marker=dict(color='grey')
            ),
            go.Scatter(
                x=datosX,
                y=current4,
                mode='lines',
                name='Current RR',
                marker=dict(color='blue')
            ),
        ]
    )
    figure_1['layout']['yaxis'] = {'range': (-200, 200)}
    return figure_1

def getTempIGBTS(data, data1, data2, data3):
    tempFL = int(data[14:16] + data[12:14], base=16)*0.0625
    tempFR = int(data1[14:16] + data1[12:14], base=16)*0.0625
    tempRL = int(data2[14:16] + data2[12:14], base=16)*0.0625
    tempRR = int(data3[14:16] + data3[12:14], base=16)*0.0625
    return tempFL, tempFR, tempRL, tempRR

def getTotalPower(data):
    power = round(int(data[0:2][0:2] + data[2:4][0:2] + data[4:6][0:2] + data[6:8][0:2],base=16)/1000,2)
    return power


def updateYawRate(data1, data2):
    PilaYawRate.pop(0)
    PilaYawRate.insert(49, data1)
    PilaYawRateRef.pop(0)
    PilaYawRateRef.insert(49, data2)
    yawRate = [int(i[10:12] + i[8:10], base=16)/1000 for i in PilaYawRate]
    yawRateRef = [int(i[10:12], base=16) for i in PilaYawRateRef]
    datosX = [i for i in range(len(yawRate))]
    figure_1 = go.Figure(
        data=[go.Scatter(
            x=datosX,
            y=yawRate,
            mode='lines',
            name='Yaw Rate',
            marker=dict(color='red')
        ),
            go.Scatter(
                x=datosX,
                y=yawRateRef,
                mode='lines',
                name='Yaw Rate Ref',
                marker=dict(color='grey')
        ),
        ]
    )
    figure_1['layout']['yaxis'] = {'range': (-3, 3)}
    return figure_1

def updateVoltages(data):
    print(data)
    minVoltage = round(float(int(data[0:2], base=16) / 51.0),3)
    totalVoltage = round(minVoltage*144,1)
    idMinVoltage = int(data[2:4][0:2], base=16)
    maxVoltage = round(float(int(data[4:6], base=16) / 51.0), 3)
    idMaxVoltage = int(data[6:8][0:2], base=16)
    minTemp = int(data[12:14][0:2], base=16)
    idMinTemp = int(data[14:16][0:2], base=16)
    maxTemp = int(data[8:10][0:2], base=16)
    idMaxTemp = int(data[10:12][0:2], base=16)
    if totalVoltage>532.8:
        colorVoltage='green'
    elif totalVoltage>512:
        colorVoltage='orange'
    else:
        colorVoltage='red'

    if maxTemp<40:
        colorTemp='green'
    elif 60>maxTemp>40:
        colorTemp='orange'
    else:
        colorTemp='red'

    return totalVoltage, minVoltage, idMinVoltage, colorVoltage, maxVoltage, idMaxVoltage, minTemp, idMinTemp, maxTemp, idMaxTemp, colorTemp


def contactorFeedbackAndAMSState(data):
    k1 = 'green' if bin(int(data[2:4][0:2], base=16))[-1] == '1' else 'grey'
    k2 = 'green' if bin(int(data[2:4][0:2], base=16))[-2] == '1' else 'grey'
    k3 = 'green' if bin(int(data[2:4][0:2], base=16))[-3] == '1' else 'grey'
    smAMS = str(data[0:2][0:2])
    smAMS = AMSSTATES.get(smAMS)
    amsLed = 'red' if int(data[4:6][0:2], base=16) != '0' else 'grey'
    errorAMS = str(int(data[4:6][0:2], base=16))
    errorAMS = AMSERRORS.get(errorAMS)
    imd = 'red' if int(data[6:8][0:2], base=16) == '1' else 'grey'
    amsMode = 'Car' if int(data[8:10][0:2], base=16) == '1' else 'Charger'
    timedOutSlvave = 'Not implemented yet'    #int(data[12:14]+data[10:12],base=16)
    current = round(-200+(1.568*int(data[14:16][0:2], base=16)),1)

    return k1, k2, k3, smAMS, errorAMS, imd, amsMode, timedOutSlvave, current, amsLed


def safetyFront(data):
    #0
    #1-Safe start 0 o 1
    #2-Front safety safe2->0, safe_inertia->1, safe_bots->3, fr->7, fl->15, safe_start->31, front_ok->3
    #2-Front safety safe2->0, safe2_inertia->1, safe_bots->3, fr->7, fl
    #2-OK->63,Inertia->60,seta_cockpit->62,BOTS->56,
    #k3
    #print(data)
    #63ok
    safe=int(data[2:4][0:2],base=16)

    if safe==63:
        frontSafetyState='Front ok'
    elif safe==62:
        frontSafetyState='Seta cockpit'
    elif safe==60:
        frontSafetyState='Safe Inertia'
    elif safe==56:
        frontSafetyState='Safe BOTS'
    elif safe==48:
        frontSafetyState='Safe FR'
    elif safe==32:
        frontSafetyState='Safe FL'
    elif safe==0:
        frontSafetyState='Front OK'
    else:
        frontSafetyState='Safe 2'


    return frontSafetyState

def dashData2(data):
    switches = bin(int(data[0:2],base=16)).zfill(8)
    loadON = "green" if str(switches)[2]=="1" else "grey"
    start = "green" if str(switches)[3]=="1" else "grey"
    powerPlus = "green" if str(switches)[4]=="1" else "grey"
    tvPlus = "green" if str(switches)[5]=="1" else "grey"
    powerMinus = "green" if str(switches)[6]=="1" else "grey"
    tvMinus = "green" if str(switches)[7]=="1" else "grey"
    state = data[10:12][0:2]
    prevState = data[12:14][0:2]

    return loadON, start, powerPlus, tvPlus, powerMinus, tvMinus, state, prevState

def safety(data, data1):
    state = str(data[12:14][0:2])
    safety = STATES.get(state)
    imd = 'red' if str(data[8:10][0:2])=='01' else 'grey'
    ams = 'red' if str(data[10:12][0:2]) == '01' else 'grey'
    plausibility = 'yellow' if str(data[14:16][0:2]) == '01' else 'grey'
    carState=str(data[0:2][0:2])
    try:
        carState = CARSTATES.get(carState)
    except KeyError:
        carState = "TETAS"
    if safety == 'Safe 4 Accu' and int(data1[4:6][0:2], base=16)==1:
        safety = 'Safe 4 Accu - INTERLOCK'

    return safety, imd, ams, plausibility, carState

def motorData(data1, data2, data3, data4):
    sw1 = int(data1[2:4]+data1[0:2],base=16)
    ls1 = int(data1[10:12]+data1[8:10]+data1[6:8]+data1[4:6],base=16)
    sw2 = int(data2[2:4]+data2[0:2], base=16)
    ls2 = int(data2[10:12] + data2[8:10] + data2[6:8] + data2[4:6], base=16)
    sw3 = int(data3[2:4]+data3[0:2], base=16)
    ls3 = int(data3[10:12] + data3[8:10] + data3[6:8] + data3[4:6], base=16)
    sw4 = int(data4[2:4]+data4[0:2], base=16)
    ls4 = int(data4[10:12] + data4[8:10] + data4[6:8] + data4[4:6], base=16)
    return sw1, ls1, sw2, ls2, sw3, ls3, sw4, ls4

def motorRPM(data1, data2, data3, data4):
    rpm1 = int(data1[6:8] + data1[4:6] + data1[2:4] + data1[0:2], base=16)*0.0000610352
    rpm2 = int(data2[6:8] + data2[4:6] + data2[2:4] + data2[0:2], base=16)*0.0000610352
    rpm3 = int(data3[6:8] + data3[4:6] + data3[2:4] + data3[0:2], base=16)*0.0000610352
    rpm4 = int(data4[6:8] + data4[4:6] + data4[2:4] + data4[0:2], base=16)*0.0000610352
    return rpm1, rpm2, rpm3, rpm4


def powerAndDCVoltage(data1, data2, data3, data4):
    print(data1)
    print(data2)
    print(data3)
    print(data4)
    #Aviso 60
    #Max 100
    temp1 = int(data1[2:4] + data1[0:2], base=16) * 0.0625
    temp2 = int(data2[2:4] + data2[0:2], base=16) * 0.0625
    temp3 = int(data3[2:4] + data3[0:2], base=16) * 0.0625
    temp4 = int(data4[2:4] + data4[0:2], base=16) * 0.0625
    power1 = int(data1[6:8] + data1[4:6], base=16) * 16
    power2 = int(data2[6:8] + data2[4:6], base=16) * 16
    power3 = int(data3[6:8] + data3[4:6], base=16) * 16
    power4 = int(data4[6:8] + data4[4:6], base=16) * 16
    return temp1, temp2, temp3, temp4, power1, power2, power3, power4

def powerFigure(data1, data2, data3, data4):
    PilaPowerFL.pop(0)
    PilaPowerFL.insert(49, data1)
    PilaPowerFR.pop(0)
    PilaPowerFR.insert(49, data2)
    PilaPowerRL.pop(0)
    PilaPowerRL.insert(49, data3)
    PilaPowerRR.pop(0)
    PilaPowerRR.insert(49, data4)
    powerFL = [int(i[6:8] + i[4:6], base=16) * 16 for i in PilaPowerFL]
    powerFR = [int(i[6:8] + i[4:6], base=16) * 16 for i in PilaPowerFR]
    powerRL = [int(i[6:8] + i[4:6], base=16) * 16 for i in PilaPowerRL]
    powerRR = [int(i[6:8] + i[4:6], base=16) * 16 for i in PilaPowerRR]
    datosX = [i for i in range(len(powerFL))]
    figure_1 = go.Figure(

        data = [go.Scatter(
            x = datosX,
            y = powerFL,
            mode = 'lines',
            name='Power FL',
            marker = dict(color = 'green')
        ),
            go.Scatter(
                x=datosX,
                y=powerFR,
                mode='lines',
                name='Power FR',
                marker=dict(color='red')
            ),
            go.Scatter(
                x=datosX,
                y=powerRL,
                mode='lines',
                name='Power RL',
                marker=dict(color='blue')
            ),
            go.Scatter(
                x=datosX,
                y=powerRR,
                mode='lines',
                name='Power RR',
                marker=dict(color='purple')
            ),
        ]
    )

    figure_1['layout']['yaxis'] = {'range': (0, 20000)}
    return figure_1


def speedAndYawRateRef(data):
    speed = round(int(data[8:10], base=16)*3.6/10, 4)
    yawRateRef = int(data[10:12], base=16)
    return speed, yawRateRef


def torqueCommands(data1, data2, data3, data4):
    tqCom1 = int(data1[14:16] + data1[12:14], base=16)
    tqCom2 = int(data2[2:4] + data2[0:2], base=16)
    tqCom3 = int(data3[14:16] + data3[12:14], base=16)
    tqCom4 = int(data4[2:4] + data4[0:2], base=16)
    return tqCom1, tqCom2, tqCom3, tqCom4


def updateSteeringWheel(data1):
    steeringWheel = round((int(data1[2:4], base=16) - 120) * 0.2083, 5)
    return steeringWheel


def dashData(data):
    power = int(data[10:12], base=16)
    tvValue = int(data[6:8], base=16)
    return power, tvValue


def tvRunning(data):
    tvRunning = 'green' if bin(int(data[14:16][0:2], base=16))[-1] == '1' else 'grey'
    return tvRunning


def updateStatuswordTranslation(data1,data2,data3,data4):
    ls1 = bin(int(data1[10:12] + data1[8:10] + data1[6:8] + data1[4:6], base=16)).removeprefix("b").zfill(32)
    ls2 = bin(int(data2[10:12] + data2[8:10] + data2[6:8] + data2[4:6], base=16)).split()[0].zfill(32)
    ls3 = bin(int(data3[10:12] + data3[8:10] + data3[6:8] + data3[4:6], base=16)).split()[0].zfill(32)
    ls4 = bin(int(data4[10:12] + data4[8:10] + data4[6:8] + data4[4:6], base=16)).split()[0].zfill(32)
    print("REVISAME")
    #print(len(ls1))
    children =html.Div(children=[
                html.Div(children=[daq.Indicator(
                            id="motor1",
                            label=statuses[i],
                            labelPosition="right",
                            color="grey" if ls1[-1-i]=='0' else 'green',
                            value=False,
                            style={'float' : 'left'}
                            )for i in range(len(statuses))
                ], className="motor1"),
                html.Div(children=[daq.Indicator(
                            id="motor2",
                            label=statuses[i],
                            labelPosition="right",
                            color="grey" if ls2[-1-i]=='0' else 'green',
                            value=False,
                            style={'float' : 'left'}
                            )for i in range(len(statuses))
                ], className="motor2"),
                html.Div(children=[daq.Indicator(
                            id="motor3",
                            label=statuses[i],
                            labelPosition="right",
                            color="grey" if ls3[-1-i]=='0' else 'green',
                            value=False,
                            style={'float' : 'left'}
                            )for i in range(len(statuses))
                ], className="motor3"),
                html.Div(children=[daq.Indicator(
                            id="motor4",
                            label=statuses[i],
                            labelPosition="right",
                            color="grey" if ls4[-1-i]=='0' else 'green',
                            value=False,
                            style={'float' : 'left'}
                            )for i in range(len(statuses))
                ])])
    return children
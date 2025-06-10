import json
from json import JSONDecodeError

PilaId0001 =['0000000000000000' for i in range(50)]
PilaId0310 =['0000000000000000' for i in range(50)]
PilaCurrentFL = ['0000000000000000' for i in range(50)]
PilaCurrentFR = ['0000000000000000' for i in range(50)]
PilaCurrentRL = ['0000000000000000' for i in range(50)]
PilaCurrentRR = ['0000000000000000' for i in range(50)]
PilaYawRate = ['0000000000000000' for i in range(50)]
PilaYawRateRef = ['0000000000000000' for i in range(50)]

def set_0310(data):
    data = dict(data)
    PilaId0310.pop(0)
    PilaId0310.insert(49, data.get('0310'))

def get_0310():
    return PilaId0310

def set_0001(data):
    PilaId0001.pop(0)
    PilaId0001.insert(49, data.get('0001'))

def set_currents(data):
    PilaCurrentFL.pop(0)
    PilaCurrentFL.insert(49, data.get('024f'))
    PilaCurrentFR.pop(0)
    PilaCurrentFR.insert(49, data.get('034f'))
    PilaCurrentRL.pop(0)
    PilaCurrentRL.insert(49, data.get('024e'))
    PilaCurrentRR.pop(0)
    PilaCurrentRR.insert(49, data.get('034e'))

def set_YawRates(data):
    PilaYawRate.pop(0)
    PilaYawRate.insert(49, data.get('0122'))
    PilaYawRateRef.pop(0)
    PilaYawRateRef.insert(49, data.get('00f2'))

def get_0001():
    return PilaId0001

def get_currentFL():
    return PilaCurrentFL

def get_currentFR():
    return PilaCurrentFR

def get_currentRL():
    return PilaCurrentRL

def get_currentRR():
    return PilaCurrentRR

def get_YawRate():
    return PilaYawRate

def get_YawRateRef():
    return PilaYawRateRef


def get_data():
    try:
        f = open('data.json')
        data = dict(json.load(f))
        set_0001(data)
        set_currents(data)
        set_YawRates(data)
        return data
    except JSONDecodeError:
        data = get_data()
        return data


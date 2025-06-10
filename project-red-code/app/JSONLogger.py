<<<<<<< HEAD
import json
import time
from json import JSONDecodeError

PilaId0001 =['0000000000000000' for i in range(50)]
PilaId0310 =['0000000000000000' for i in range(50)]
PilaCurrentFL = ['0000000000000000' for i in range(50)]
PilaCurrentFR = ['0000000000000000' for i in range(50)]
PilaCurrentRL = ['0000000000000000' for i in range(50)]
PilaCurrentRR = ['0000000000000000' for i in range(50)]

def set_0310(data):
    data = dict(data)
    PilaId0310.pop(0)
    PilaId0310.insert(49, data.get('0310'))

def get_0310():
    return PilaId0310

def set_0001(data):
    data = dict(data)
    PilaId0001.pop(0)
    PilaId0001.insert(49, data.get('0001'))

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

def get_data():
    try:
        f = open('data.json')
        data = json.load(f)
        set_0001(data)
        return data
    except JSONDecodeError:
        data = get_data()
        return data

nombreLog = 'log_' + str(time.time()) + '.json'

with open(nombreLog, "w") as outfile:
    json.dump(dictionary, outfile)


=======
import json
import time
from json import JSONDecodeError

PilaId0001 =['0000000000000000' for i in range(50)]
PilaId0310 =['0000000000000000' for i in range(50)]
PilaCurrentFL = ['0000000000000000' for i in range(50)]
PilaCurrentFR = ['0000000000000000' for i in range(50)]
PilaCurrentRL = ['0000000000000000' for i in range(50)]
PilaCurrentRR = ['0000000000000000' for i in range(50)]

def set_0310(data):
    data = dict(data)
    PilaId0310.pop(0)
    PilaId0310.insert(49, data.get('0310'))

def get_0310():
    return PilaId0310

def set_0001(data):
    data = dict(data)
    PilaId0001.pop(0)
    PilaId0001.insert(49, data.get('0001'))

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

def get_data():
    try:
        f = open('data.json')
        data = json.load(f)
        set_0001(data)
        return data
    except JSONDecodeError:
        data = get_data()
        return data

nombreLog = 'log_' + str(time.time()) + '.json'

with open(nombreLog, "w") as outfile:
    json.dump(dictionary, outfile)


>>>>>>> 17b1810be65e2c353afb1d112575b85b5c4866ed

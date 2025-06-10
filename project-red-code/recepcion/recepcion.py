import paho.mqtt.client as mqtt
import redis
from datetime import datetime

# Conexión a Redis
client = redis.Redis(host='redis', port=6379, health_check_interval=30, decode_responses=True)

# Diccionario de claves iniciales

dictionary = {
    "0310": "2306124567210341",
    "0090": "2304124567210341",
    "00f0": "2304124567210000",
    "00f1": "2304124567210000",
    "00f2": "2304124567210000",
    "00a2": "0000000000000000",
    "0001": "2304124567210341",
    "0311": "BE12456721034178",
    "01cf": "0000010000000000",
    "02cf": "2783563298457345",
    "01ce": "0794385729875348",
    "02ce": "3452704389528393",
    "024f": "0000000000000000",
    "034f": "0000000000000000",
    "024e": "0000000000000000",
    "034e": "0000000000000000",
    "028f": "0000000000000000",
    "038f": "0000000000000000",
    "028e": "0000000000000000",
    "038e": "0000000000000000",
    "020e": "0000000000000000",
    "040e": "0000000000000000",
    "020f": "0000000000000000",
    "040f": "0000000000000000",
    "0122": "0000000000000000",
    "0181": "0000000000000000",
    "0101": "0000000000000000",
    "0102": "0000000000000000",
    "0103": "0000000000000000",
    "0104": "0000000000000000",
    "0105": "0000000000000000",
    "0106": "0000000000000000",
    "0107": "0000000000000000",
    "0108": "0000000000000000",
    "0109": "0000000000000000",
    "010a": "0000000000000000",
    "010b": "0000000000000000",
    "1101": "0000000000000000",
    "1102": "0000000000000000",
    "1103": "0000000000000000",
    "1104": "0000000000000000",
    "1105": "0000000000000000",
    "1106": "0000000000000000",
    "1107": "0000000000000000",
    "1108": "0000000000000000",
    "1109": "0000000000000000",
    "110a": "0000000000000000",
    "110b": "0000000000000000",
}

# Inicializar claves en Redis
for i in dictionary:
    client.set(i, dictionary[i])

print('Comenzamos a escuchar por MQTT...')

# Callback cuando se conecta al broker
def on_connect(mqttc, userdata, flags, rc):
    print("Conectado al broker con código:", rc)
    mqttc.subscribe("telemetry")

# Callback cuando se recibe un mensaje
def on_message(mqttc, userdata, msg):
    try:
        payload = msg.payload
        #print(f"Payload (bytes): {payload}")
        payload_str = payload.decode('utf-8')
        #print(f"Payload (str): {payload_str}")
        if payload_str.startswith("b'") and payload_str.endswith("'"):
            payload_str = payload_str[2:-1]
        payload_str = payload_str.ljust(20, '0')

        #print(payload_str)
        id = payload_str[0:4]
        valor = payload_str[4:]  # Limpieza como hacías antes
        client.set(id, valor)
        #print(msg.payload)
        if payload_str[0:4] == "0001":
            timestamp = datetime.now().isoformat()
            print(f"[{timestamp}],{payload_str}")

    except Exception as e:
        print(f"Error procesando mensaje: {e}")

# Conectar al broker local
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("mqtt", 1883, 60)
mqttc.loop_forever()

import paho.mqtt.client as mqtt
from datetime import datetime

# Callback cuando se conecta al broker
def on_connect(mqttc, userdata, flags, rc):
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] Suscrito al tópico: telemetry")
    mqttc.subscribe("telemetry")

# Callback cuando se recibe un mensaje
def on_message(mqttc, userdata, msg):
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] Mensaje recibido en '{msg.topic}': {msg.payload.decode('utf-8', errors='replace')}")

# Crear cliente MQTT
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# Conectar al broker y mantener la conexión
mqttc.connect("104.197.36.231", 1883, 60)
mqttc.loop_forever()

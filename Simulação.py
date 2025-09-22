//pip install paho-mqtt fazer no cmd

import paho.mqtt.client as mqtt
import time
import random
import json

# ===================== CONFIG MQTT =====================
BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC_GPS = "moto/gps"
TOPIC_PROX = "moto/proximidade"
TOPIC_ACCEL = "moto/movimento"
TOPIC_ALARME = "moto/alarme"

# ===================== CALLBACKS =====================
def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker MQTT:", BROKER)
    client.subscribe(TOPIC_ALARME)  # escuta comandos para o buzzer

def on_message(client, userdata, msg):
    if msg.topic == TOPIC_ALARME:
        if msg.payload.decode() == "1":
            print("🚨 Buzzer LIGADO (alarme acionado!)")
        else:
            print("✅ Buzzer DESLIGADO")

# ===================== CONFIG CLIENT =====================
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)

client.loop_start()

# ===================== LOOP DE SIMULAÇÃO =====================
try:
    while True:
        # Simulação GPS
        lat = -23.56 + random.uniform(-0.001, 0.001)  # perto da Av. Paulista
        lng = -46.65 + random.uniform(-0.001, 0.001)
        gps_data = {"lat": lat, "lng": lng}
        client.publish(TOPIC_GPS, json.dumps(gps_data))
        print("📡 GPS:", gps_data)

        # Simulação Ultrassônico (vaga de 40 cm)
        distancia = random.uniform(10, 60)
        client.publish(TOPIC_PROX, str(distancia))
        print("📏 Proximidade:", round(distancia, 2), "cm")

        # Simulação Acelerômetro
        accel_data = {
            "x": random.uniform(-1, 1),
            "y": random.uniform(-1, 1),
            "z": random.uniform(9, 10) if random.random() > 0.1 else random.uniform(15, 20)  # z "explodindo" = movimento suspeito
        }
        client.publish(TOPIC_ACCEL, json.dumps(accel_data))
        print("📈 Movimento:", accel_data)

        # Se movimento suspeito -> aciona buzzer
        if accel_data["z"] > 15:
            client.publish(TOPIC_ALARME, "1")
        else:
            client.publish(TOPIC_ALARME, "0")

        print("-" * 40)
        time.sleep(2)

except KeyboardInterrupt:
    print("Simulação encerrada.")
    client.loop_stop()
    client.disconnect()


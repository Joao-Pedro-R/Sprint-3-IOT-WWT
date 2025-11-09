import paho.mqtt.client as mqtt
import time, json, random

BROKER = "broker.hivemq.com"
PORT = 1883

client = mqtt.Client()
client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    lat, lng = -23.5620, -46.6540  # posição da oficina
    while True:
        # GPS fixo (não deveria se mover)
        client.publish("moto/gps", json.dumps({"lat": lat, "lng": lng}))
        client.publish("moto/proximidade", "30")

        # Simula uma possível vibração ou deslocamento indevido
        z_val = random.choice([9.8, 10, 18])  # às vezes “explode”
        accel = {"x": random.uniform(-0.1, 0.1),
                 "y": random.uniform(-0.1, 0.1),
                 "z": z_val}
        client.publish("moto/movimento", json.dumps(accel))

        if z_val > 15:
            print("🚨 Movimento detectado na oficina! Alarme acionado.")
            client.publish("moto/alarme", "1")
        else:
            client.publish("moto/alarme", "0")

        time.sleep(2)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()

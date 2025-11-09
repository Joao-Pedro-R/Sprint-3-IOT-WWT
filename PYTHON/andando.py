import paho.mqtt.client as mqtt
import time, random, json

BROKER = "broker.hivemq.com"
PORT = 1883

client = mqtt.Client()
client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    while True:
        # GPS variando
        lat = -23.56 + random.uniform(-0.001, 0.001)
        lng = -46.65 + random.uniform(-0.001, 0.001)
        client.publish("moto/gps", json.dumps({"lat": lat, "lng": lng}))

        # Distância próxima de 40 cm
        dist = random.uniform(35, 45)
        client.publish("moto/proximidade", str(dist))

        # Movimento leve (sem alarme)
        accel = {"x": random.uniform(-1, 1),
                 "y": random.uniform(-1, 1),
                 "z": random.uniform(9, 10)}
        client.publish("moto/movimento", json.dumps(accel))
        client.publish("moto/alarme", "0")

        print("🏍️ Moto em movimento — GPS:", lat, lng)
        time.sleep(2)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()

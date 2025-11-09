import paho.mqtt.client as mqtt
import time, json

BROKER = "broker.hivemq.com"
PORT = 1883

client = mqtt.Client()
client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    lat, lng = -23.5610, -46.6530  # ponto fixo
    while True:
        client.publish("moto/gps", json.dumps({"lat": lat, "lng": lng}))
        client.publish("moto/proximidade", "50")
        accel = {"x": 0.01, "y": 0.01, "z": 9.81}
        client.publish("moto/movimento", json.dumps(accel))
        client.publish("moto/alarme", "0")

        print("🅿️ Moto parada — posição fixa")
        time.sleep(2)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()

import paho.mqtt.client as mqtt
import sqlite3
import json

BROKER = "broker.hivemq.com"
PORT = 1883
TOPICS = ["moto/gps", "moto/proximidade", "moto/movimento", "moto/alarme"]

conn = sqlite3.connect("iot_motos.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS historico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topico TEXT,
    valor TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

def on_connect(client, userdata, flags, rc):
    print("Conectado ao MQTT!")
    for t in TOPICS:
        client.subscribe(t)

def on_message(client, userdata, msg):
    valor = msg.payload.decode()
    print(f"[{msg.topic}] {valor}")

    cursor.execute("INSERT INTO historico (topico, valor) VALUES (?, ?)", (msg.topic, valor))
    conn.commit()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)

print("Aguardando mensagens...")
client.loop_forever()

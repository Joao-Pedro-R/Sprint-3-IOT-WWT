#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <TinyGPS++.h>
#include <HardwareSerial.h>

const char* ssid = "FIAP-IOT";        
const char* password = "****";  
const char* mqtt_server = "broker.hivemq.com"; 

// Tópicos MQTT
const char* topico_gps = "esp32/moto/gps";
const char* topico_proximdade = "esp32/moto/proximidade";
const char* topico_movimento = "esp32/moto/movimento";
const char* topico_alarme = "esp32/moto/alarme";

WiFiClient espClient;
PubSubClient client(espClient);

TinyGPSPlus gps;
HardwareSerial gpsSerial(1);
#define GPS_RX 16
#define GPS_TX 17

const int trigPin = 5;
const int echoPin = 18;

Adafruit_MPU6050 mpu;

const int buzzerPin = 19;

long duration;
float distance;

void setup_wifi() {
  delay(10);

  Serial.println();
  Serial.print("Conectando ao ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando ao Wi-Fi...");
  }

  
  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {

  while (!client.connected()) {
    Serial.print("Tentando conexão MQTT...");
    String clientId = "ESP32ClientMoto";
    clientId += String(random(0xffff), HEX);

    if (client.connect(clientId.c_str())) {
      Serial.println("conectado");
      client.publish("SPRINT3DDJ/IN", "Iniciando transferencias...");
      client.subscribe("SPRINT3DDJ/OUT");
    } else {
      Serial.print("falhou, rc=");
      Serial.print(client.state());
      Serial.println(" tente novamente em 5 segundos");
      
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Mensagem recebida [");
  Serial.print(topic);
  Serial.print("]: ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void setup() {
  Serial.begin(115200);

  setup_wifi();
  client.setServer(mqtt_server, 1883);

  gpsSerial.begin(9600, SERIAL_8N1, GPS_RX, GPS_TX);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(buzzerPin, OUTPUT);

  Wire.begin(21, 22);

  if (!mpu.begin()) {
    Serial.println("Erro ao inicializar o MPU6050!");
    while (1) delay(10);
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  Serial.println("Sistema pronto!");
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
    if (gps.location.isUpdated()) {
      String gpsData = "{" 
        "\"lat\": " + String(gps.location.lat(), 6) + 
        ", \"lng\": " + String(gps.location.lng(), 6) + 
        "}";
      client.publish("moto/gps", gpsData.c_str());
      Serial.println("GPS enviado: " + gpsData);
    }
  }

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2; // cm
  String distData = String(distance);
  client.publish("moto/proximidade", distData.c_str());
  Serial.println("Distância enviada: " + distData + " cm");

  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  String accelData = "{"
    "\"x\": " + String(a.acceleration.x) +
    ", \"y\": " + String(a.acceleration.y) +
    ", \"z\": " + String(a.acceleration.z) +
    "}";
  client.publish("moto/movimento", accelData.c_str());
  Serial.println("Accel enviado: " + accelData);

  if (abs(a.acceleration.z) > 15) {
    digitalWrite(buzzerPin, HIGH);
    client.publish("moto/alarme", "1");
    Serial.println("⚠️ ALERTA: Movimento suspeito! Buzzer acionado!");
  } else {
    digitalWrite(buzzerPin, LOW);
    client.publish("moto/alarme", "0");
  }

  Serial.println("-----------------------------");
  delay(2000);
}

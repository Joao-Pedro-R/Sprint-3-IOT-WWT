# Sprint-3-IOT-WWT
Link Wowki: https://wokwi.com/projects/442760478935109633

# 🚀 IoT - Monitoramento de Motos em Pátio

Este projeto demonstra um **sistema IoT de monitoramento de motos** utilizando sensores físicos (ou simulados), comunicação MQTT e um **dashboard no Node-RED** para visualização em tempo real.

---

## 📖 Visão Geral
A solução monitora o status de motos em um pátio através de diferentes sensores, enviando os dados para um **broker MQTT**, que posteriormente são consumidos pelo **Node-RED** e exibidos em um dashboard web.

O sistema detecta:
- 📍 **Localização GPS** da moto.  
- 📏 **Distância/proximidade** da vaga usando ultrassônico.  
- 📈 **Movimento/posição** via acelerômetro.  
- 🚨 **Alarme** sonoro (simulado com buzzer).  

---

## 🔧 Tecnologias Utilizadas
- **ESP32 / Arduino IDE** → microcontrolador para ler sensores e publicar via MQTT.  
- **Sensores**:
  - GPS NEO-6M
  - Ultrassônico HC-SR04
  - Acelerômetro MPU6050
  - Buzzer (atuador)
- **Protocolos**: MQTT (via [HiveMQ Broker](https://www.hivemq.com/public-mqtt-broker/))  
- **Node-RED + Dashboard** → exibição dos dados e testes de casos de uso.  
- **Python + Paho-MQTT** (opcional) → simulação de dados.  

---

## 📡 Arquitetura
```mermaid
graph TD;
    ESP32["ESP32 + Sensores"]
    MQTT["Broker MQTT (HiveMQ)"]
    NodeRED["Node-RED"]
    Dashboard["Dashboard Web"]

    ESP32 -->|Publica dados| MQTT
    Python["Python Simulator"] -->|[NO CASO DE TESTE COM SIMULADORES WEB]Publica dados| ESP32
    MQTT --> NodeRED
    NodeRED --> Dashboard

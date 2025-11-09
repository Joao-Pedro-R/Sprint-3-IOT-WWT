import org.eclipse.paho.client.mqttv3.*;
import com.google.gson.Gson;
import java.util.Random;

public class MqttMotoIntegration {

    private static final String BROKER = "tcp://broker.hivemq.com:1883";
    private static final String CLIENT_ID = "java-moto-client-" + System.currentTimeMillis();
    private static final String TOPIC_GPS = "moto/gps";
    private static final String TOPIC_ALARME = "moto/alarme";

    public static void main(String[] args) {
        try {
            MqttClient client = new MqttClient(BROKER, CLIENT_ID);
            MqttConnectOptions options = new MqttConnectOptions();
            options.setCleanSession(true);

            // Callback de eventos MQTT
            client.setCallback(new MqttCallback() {
                @Override
                public void connectionLost(Throwable cause) {
                    System.out.println("❌ Conexão perdida: " + cause.getMessage());
                }

                @Override
                public void messageArrived(String topic, MqttMessage message) {
                    System.out.println("📩 Mensagem recebida: " + topic + " → " + new String(message.getPayload()));
                }

                @Override
                public void deliveryComplete(IMqttDeliveryToken token) {
                    // opcional
                }
            });

            client.connect(options);
            System.out.println("✅ Conectado ao broker MQTT: " + BROKER);

            client.subscribe(TOPIC_ALARME);
            System.out.println("📡 Assinado no tópico: " + TOPIC_ALARME);

            Random random = new Random();
            Gson gson = new Gson();

            while (true) {
                // Simula coordenadas GPS próximas à Av. Paulista
                double lat = -23.56 + random.nextDouble() * 0.002 - 0.001;
                double lng = -46.65 + random.nextDouble() * 0.002 - 0.001;

                String gpsJson = gson.toJson(new GPS(lat, lng));
                MqttMessage msg = new MqttMessage(gpsJson.getBytes());
                msg.setQos(1);

                client.publish(TOPIC_GPS, msg);
                System.out.println("📤 GPS publicado: " + gpsJson);

                Thread.sleep(2000);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Classe auxiliar para gerar JSON do GPS
    static class GPS {
        double lat;
        double lng;
        GPS(double lat, double lng) {
            this.lat = lat;
            this.lng = lng;
        }
    }
}

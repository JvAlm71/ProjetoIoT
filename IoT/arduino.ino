#include "DHT.h"
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

#define DHTPIN 22     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321

const char* ssid = "ROTA 69 2G";
const char* password = "SADDAN69";

// Configurações do broker MQTT (substitua pelos dados do seu ambiente Kapua)
const char* mqttServer = "143.107.232.252"; 
const int mqttPort = 7043;
const char* mqttUser = "mqtt";
const char* mqttPassword = "mqtt@123";

DHT dht(DHTPIN, DHTTYPE);

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  Serial.println(F("DHTxx test!"));
  dht.begin();


  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando ao WiFi...");
  }

  Serial.println("Conectado ao WiFi");
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  while (!client.connected()) {
    if (client.connect("client-id-kura", mqttUser, mqttPassword)) {
      Serial.println("Conectado ao broker MQTT");
    } else {
      Serial.print("Falha na conexão ao broker MQTT, rc=");
      Serial.println(client.state());
      // Serial.println(client.)
      delay(2000);
    }
  }
}

void loop() {
  // Wait a few seconds between measurements.

  delay(6000);
  if (!client.connected()){
    reconnect();
  }

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  // Compute heat index in Fahrenheit (the default)
  float hif = dht.computeHeatIndex(f, h);
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));
  Serial.print(f);
  Serial.print(F("°F  Heat index: "));
  Serial.print(hic);
  Serial.print(F("°C "));
  Serial.print(hif);
  Serial.println(F("°F"));
  StaticJsonDocument<200> doc;
  JsonObject metrics = doc.createNestedObject("metrics");
  metrics["temperatura"] = t;
  metrics["umidade"] = h;
  metrics["sensacao_termica"] = hic;

  char jsonBuffer[256];
  serializeJson(doc, jsonBuffer);
  char * topico = "account-kura/client-id-kura/sensor/dados";
  bool envio = client.publish(topico, jsonBuffer);
  
  if (envio) {
    Serial.println("JSON enviados com sucesso");
  } else {
    Serial.println("Falha ao enviar os dados");
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  // Função de callback chamada quando uma mensagem é recebida no tópico subscrito
  Serial.print("Mensagem recebida no tópico: ");
  Serial.println(topic);

  Serial.print("Payload: ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void reconnect() {
   while (!client.connected()) {
      Serial.println("Tentando reconectar ao broker MQTT...");
      if (client.connect("ESP32", mqttUser, mqttPassword)) {
         Serial.println("Conectado ao broker MQTT");
      } else {
         Serial.print("Falha na conexão ao broker MQTT, rc=");
         Serial.println(client.state());
         delay(5000);  // Espere 5 segundos antes de tentar novamente
      }
   }
}

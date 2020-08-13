#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* SSID = "<SSID>";
const char* PSK = "<PSK>";
const char* MQTT_BROKER = "<HOSTNAME>";
const char* MQTT_USERNAME = "<USER>";
const char* MQTT_PASSWORD = "<PASSWORD>";

WiFiClient espClient;
PubSubClient client(espClient);

#include <SoftwareSerial.h>
SoftwareSerial mySerial(5, 4); // RX, TX

void setup()
{
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Native USB only
  }

  setup_wifi();
  client.setServer(MQTT_BROKER, 1883);

  mySerial.begin(9600);
}

void setup_wifi() {
    WiFi.begin(SSID, PSK);

    while (WiFi.status() != WL_CONNECTED) {
        delay(100);
    }

    Serial.print("connected to WIFI - IP: ");
    Serial.println(WiFi.localIP());
}

float v;
String value;

void loop() {
  if (mySerial.available() > 0){
    v = mySerial.parseFloat();
    value = String(v);
    Serial.println(value);

    if (!client.connected()) {
      while (!client.connected()) {
        client.connect("ESP8266Client", MQTT_USERNAME, MQTT_PASSWORD);
        delay(100);
      }
    }
    client.loop();

    int str_len = value.length() + 1;
    char char_array[str_len];
    value.toCharArray(char_array, str_len);
    client.publish("/kitchen/pressure", char_array);

  }
  delay(15000);
}
#include <ESP8266WiFi.h>
//#include <Adafruit_NeoPixel.h>
#include <DHT.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>

// --------------------------------------------------------------------------------------------
//        UPDATE CONFIGURATION TO MATCH YOUR ENVIRONMENT
// --------------------------------------------------------------------------------------------

// Watson IoT connection details
#define MQTT_HOST "ORGA_ID.messaging.internetofthings.ibmcloud.com"
#define MQTT_PORT 1883
#define MQTT_USER "use-token-auth"
#define MQTT_TOPIC "iot-2/evt/status/fmt/json"
#define MQTT_TOPIC_CMD "iot-2/cmd/display/fmt/json"
#define DEVICE_ID "DEV_ID"
#define MQTT_DEVICEID "d:ORGA_ID:DEV_TYPE:DEV_ID"
#define MQTT_TOKEN "TOKEN GOES HERE"

// DHT Sensors
#define DHT_PIN_01 4     // what digital pin we're connected to
#define DHT_PIN_02 12    // what digital pin we're connected to

// Specify DHT11 (Blue) or DHT22 (White) sensor
#define DHTTYPE DHT22
//#define NEOPIXEL_TYPE NEO_RGB + NEO_KHZ800

// Temperatures to set LED by (assume temp in C)
#define ALARM_COLD 0.0
#define ALARM_HOT 30.0
#define WARN_COLD 10.0
#define WARN_HOT 25.0


// Add WiFi connection information
char ssid[] = "ssid";     //  your network SSID (name)
char pass[] = "pw";  // your network password



// --------------------------------------------------------------------------------------------
//        SHOULD NOT NEED TO CHANGE ANYTHING BELOW THIS LINE
// --------------------------------------------------------------------------------------------
//Adafruit_NeoPixel pixel = Adafruit_NeoPixel(1, RGB_PIN, NEOPIXEL_TYPE);
const int numSensors = 2;  // number of connected sensors, must be in dhts!

DHT dhts[numSensors] = {
  DHT(DHT_PIN_01, DHTTYPE),
  DHT(DHT_PIN_02, DHTTYPE)
  };


String sensor_IDs[200] = { "sensor01", "sensor02" };

// MQTT objects
void callback(char* topic, byte* payload, unsigned int length);
WiFiClient wifiClient;
PubSubClient mqtt(MQTT_HOST, MQTT_PORT, callback, wifiClient);

// variables to hold data
StaticJsonBuffer<100> jsonBuffer;
JsonObject& payload = jsonBuffer.createObject();
JsonObject& status = payload.createNestedObject("d");
static char msg[50];

float h = 0.0;
float t = 0.0;


void callback(char* topic, byte* payload, unsigned int length) {
  // handle message arrived
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.println("] ");
}

void setup() {
 // Start serial console
  Serial.begin(115200);
  Serial.setTimeout(2000);
  while (!Serial) { }
  Serial.println();
  Serial.println("ESP8266 Sensor Application");

  // Start WiFi connection
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi Connected");

  // Start connected devices
   for (int i=0; i < numSensors; i++){
      dhts[i].begin();
      delay(10);
   }
  //pixel.begin();

  // Connect to MQTT - IBM Watson IoT Platform
  if (mqtt.connect(MQTT_DEVICEID, MQTT_USER, MQTT_TOKEN)) {
    Serial.println("MQTT Connected");
    mqtt.subscribe(MQTT_TOPIC_CMD);

  } else {
    Serial.println("MQTT Failed to connect!");
    ESP.reset();
  }
}

void loop() {
  mqtt.loop();
  while (!mqtt.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (mqtt.connect(MQTT_DEVICEID, MQTT_USER, MQTT_TOKEN)) {
      Serial.println("MQTT Connected");
      mqtt.subscribe(MQTT_TOPIC_CMD);
      mqtt.loop();
    } else {
      Serial.println("MQTT Failed to connect!");
      delay(5000);
    }
  }
   for (int i=0; i < numSensors; i++){
      Serial.print("Reading sensor: ");
      Serial.println(sensor_IDs[i]);
      h = dhts[i].readHumidity();
      delay(100);
      t = dhts[i].readTemperature(); // uncomment this line for centigrade
      // t = dht.readTemperature(true); // uncomment this line for Fahrenheit

      // Check if any reads failed and exit early (to try again).
      if (isnan(h) || isnan(t)) {
        Serial.println("Failed to read from DHT sensor!");
      } else {
    
        // Send data to Watson IoT Platform
        status["temp"] = t;
        status["humidity"] = h;
        status["sensorID"] = sensor_IDs[i];
        payload.printTo(msg, 100);
        Serial.println(msg);
        if (!mqtt.publish(MQTT_TOPIC, msg)) {
          Serial.println("MQTT Publish failed");
        }
      }
      
      // Pause - but keep polling MQTT for incoming messages
      for (int i = 0; i < 2; i++) {
        mqtt.loop();
        delay(1000);
      }

   }

  




}

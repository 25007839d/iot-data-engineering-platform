#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT11

#define SENSOR_PIN 18      // LM393 DO Pin
#define BUZZER_PIN 23

// WiFi Details
const char* ssid = "AirFiber-cha5Es";
const char* password = "Pass@123";

// API URL
const char* apiUrl = "https://iot-api-6vuj.onrender.com/sensor";

DHT dht(DHTPIN, DHTTYPE);

void setup() {

  Serial.begin(115200);

  dht.begin();

  pinMode(SENSOR_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  digitalWrite(BUZZER_PIN, LOW);

  Serial.println("================================");
  Serial.println("IoT Sensor Starting...");
  Serial.println("================================");

  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi Connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  Serial.println("================================");
}

void loop() {

  // Read Temperature
  float temperature = dht.readTemperature();

  if (isnan(temperature)) {
    Serial.println("DHT11 Read Failed");
    delay(2000);
    return;
  }

  // Read Obstacle Sensor
  int sensorState = digitalRead(SENSOR_PIN);

  Serial.print("Sensor State: ");
  Serial.println(sensorState);

  int vibration = 0;
  int current = 0;

  // Your sensor behavior:
  // Object Detected = 1
  // No Object = 0

  if (sensorState == HIGH) {

    vibration = 1;
    current = 1;

    digitalWrite(BUZZER_PIN, HIGH);

    Serial.println("Obstacle Detected");
  }
  else {

    vibration = 0;
    current = 0;

    digitalWrite(BUZZER_PIN, LOW);

    Serial.println("No Obstacle");
  }

  // Create JSON Payload
  String payload = "{";
  payload += "\"temperature\":" + String(temperature, 2) + ",";
  payload += "\"vibration\":" + String(vibration) + ",";
  payload += "\"current\":" + String(current);
  payload += "}";

  Serial.println("--------------------------------");
  Serial.println("Payload:");
  Serial.println(payload);

  // API Call
  if (WiFi.status() == WL_CONNECTED) {

    HTTPClient http;

    http.begin(apiUrl);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(payload);

    Serial.print("HTTP Response Code: ");
    Serial.println(httpResponseCode);

    String response = http.getString();

    Serial.print("Response: ");
    Serial.println(response);

    http.end();

  } else {

    Serial.println("WiFi Disconnected");
  }

  Serial.println("--------------------------------");
  Serial.println();

  delay(10000); // Send every 10 seconds
}
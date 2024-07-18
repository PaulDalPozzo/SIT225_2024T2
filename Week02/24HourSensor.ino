/*
  Paul Dal Pozzo
  s214527809
  SIT225 - Data Capture Technologies
  Week 02
  Task 2.1P
  This code is an editted of my SIT210 Task 2.1P code minus the ThingSpeak connection
*/

#include "DHT.h"

#define DHTPIN 2        // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT type 11 or 22
DHT dht(DHTPIN, DHTTYPE);

const int INTERVAL_TIME = 600000;   // 10 minutes = 10 minutes * 60 seconds * 1000 milliseconds
const int SHUTDOWN_TIME = 86400000;   // 24 hours = 24 hours * 60 minutes * 60 seconds * 1000 milliseconds
// Initialize our values
float temperature = 0;
float humidity = 0;
float heatIndex = 0;
unsigned long currentMillis = 0;
unsigned long previousMillis = 0;

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  // timer to run on INTERVAL_TIME
  currentMillis = millis();
  if (currentMillis < INTERVAL_TIME + previousMillis) return;
  previousMillis = currentMillis;
  
  if (previousMillis < SHUTDOWN_TIME){
    readSensor();
    printData();
  }
}

void readSensor() {
  // read data
  temperature = dht.readTemperature();    // Celsius is default
  humidity = dht.readHumidity();
  heatIndex = dht.computeHeatIndex(temperature, humidity, false);
}

void printData() {
  // if there is no reading, record a 0
  if (isnan(temperature)) {
    temperature = 0;
  }
  if (isnan(humidity)) {
    humidity = 0;
  }
  if (isnan(heatIndex)) {
    heatIndex = 0;
  }

  // print to serial to be read by python
  Serial.print(String(temperature));
  Serial.print(",");
  Serial.print(String(humidity));
  Serial.print(",");
  Serial.println(String(heatIndex));
  Serial.flush();
}

#include "thingProperties.h"
#include <Arduino_LSM6DS3.h>

const int INTERVAL_TIME = 1000;   // 1 seconds

void setup() {
  Serial.begin(9600);
  delay(1500); 

  // Defined in thingProperties.h
  initProperties();

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();
}

void loop() {
  ArduinoCloud.update();
  // read accelero data
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x_axis, y_axis, z_axis);
  }
    
  delay(INTERVAL_TIME);
}

void onXAxisChange()  {
}

void onYAxisChange()  {
}

void onZAxisChange()  {
}
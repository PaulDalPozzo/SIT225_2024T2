/*
  Paul Dal Pozzo
  s214527809
  SIT225 - Data Capture Technologies
  Week 03
  Task 3.1P
*/

#include "thingProperties.h"
#include <Arduino_LSM6DS3.h>

const int INTERVAL_TIME = 1000;   // 1 seconds
float x, y, z;

void setup() {
  Serial.begin(9600); // set baud rate
  while (!Serial);  // wait for port to init

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  // Defined in thingProperties.h
  initProperties();

  // Connect to Arduino IoT Cloud
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();
}

void loop() {
  ArduinoCloud.update();

  // read accelero data
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
    //Serial.print("X: ");
    //Serial.print(x);
    //Serial.print(" Y: ");
    //Serial.print(y);
    //Serial.print(" Z: ");
    //Serial.println(z);
  }

  delay(INTERVAL_TIME);
}

/*
  Since XAxis is READ_WRITE variable, onXAxisChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onXAxisChange()  {
  Serial.println("X Property Added");
}
/*
  Since YAxis is READ_WRITE variable, onYAxisChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onYAxisChange()  {
  Serial.println("Y Property Added");
}
/*
  Since ZAxis is READ_WRITE variable, onZAxisChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onZAxisChange()  {
  Serial.println("Z Property Added");
}
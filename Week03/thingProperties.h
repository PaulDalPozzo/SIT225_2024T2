#include "arduino_secrets.h"
#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>

const char SSID[]     = SECRET_SSID;    // Network SSID (name)
const char PASS[]     = SECRET_OPTIONAL_PASS;    // Network password (use for WPA, or use as key for WEP)

void onXAxisChange();
void onYAxisChange();
void onZAxisChange();

float x_axis;
float y_axis;
float z_axis;

void initProperties(){

  ArduinoCloud.addProperty(x_axis, READWRITE, ON_CHANGE, onXAxisChange);
  ArduinoCloud.addProperty(y_axis, READWRITE, ON_CHANGE, onYAxisChange);
  ArduinoCloud.addProperty(z_axis, READWRITE, ON_CHANGE, onZAxisChange);

}

WiFiConnectionHandler ArduinoIoTPreferredConnection(SSID, PASS);

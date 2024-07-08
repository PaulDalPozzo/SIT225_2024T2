/*
  Paul Dal Pozzo
  s214527809
  SIT225 - Data Capture Technologies
  Week 01
  Task 1.1P
*/

int receivedFromPython;
int sendToPython = 1;

void setup() 
{
  pinMode(LED_BUILTIN, OUTPUT);     // configure LED pin to be output
  digitalWrite(LED_BUILTIN, LOW);   // intialising the LED to off

  Serial.begin(9600);
}

void loop() 
{
  // wait for serial to receive data from python script
  while (!Serial.available()) {}
  // read data from the serial
  receivedFromPython = Serial.readString().toInt();
  // blink the value that was sent
  blink(receivedFromPython);

  // assign a random value between 1 and 10, excluding 10
  sendToPython = random(1, 10);   
  // push data through serial channel
  Serial.print(sendToPython);
  Serial.flush();
}

void blink(int repeats)
{
  if (repeats == 0) return;

  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
  blink(repeats - 1);
}

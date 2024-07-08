#  Paul Dal Pozzo
#  s214527809
#  SIT225 - Data Capture Technologies
#  Week 01
#  Task 1.1P

import serial
import random
from datetime import datetime

def waiting(secondsLeft):
    if secondsLeft > 0:
        time.sleep(1)
        waiting(secondsLeft - 1)

def getTimeStamp():
    now = datetime.now()
    timeStamp = now.strftime("%H:%M:%S")
    return timeStamp

# set the baud rate to the same one used in Arduino code
baud_rate = 9600
# set serial port
ser = serial.Serial('COM3', baud_rate, timeout=5)
sleeptime = 0

while True:
    # random number between 1 and 5
    sendToArduino = random.randint(1, 5)
    data = ser.write(bytes(str(sendToArduino), 'utf-8'))
    
    # print sent data with timestamp
    print("{0}: Sent to Arduino --------> {1} ({2} bytes)".format(getTimeStamp(), sendToArduino, data))
    # wait for Ardiuno to perform blink and sent data
    sleeptime = sendToArduino * 2
    waiting(sleeptime)
    
    # print recieved data with timestamp
    receiveFromArduino = ser.readline().decode("utf-8")
    print("{0}: Received from Arduino <-- {1}".format(getTimeStamp(), receiveFromArduino))

    try:
        # sleeps for that number of seconds
        sleeptime = int(receiveFromArduino)
        print("{0}: Sleeping for {1} seconds.".format(getTimeStamp(), receiveFromArduino))
        waiting(sleeptime)
        print("{0}: Awake and ready to send another number".format(getTimeStamp()))
    except:
        print("{0}: Data received from Arduino was not a valid integer".format(getTimeStamp()))

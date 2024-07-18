#  Paul Dal Pozzo
#  s214527809
#  SIT225 - Data Capture Technologies
#  Week 02
#  Task 2.1P

import serial
import random
import time
import csv
import os.path
from datetime import datetime

def waiting(secondsLeft):
    if secondsLeft > 0:
        time.sleep(1)
        waiting(secondsLeft - 1)

def getTimeStamp():
    now = datetime.now()
    #YearMonthDayHourMinuteSecond
    timeStamp = now.strftime("%Y%m%d%H%M%S")
    return timeStamp


# set the baud rate to the same one used in Arduino code
baud_rate = 9600
# set serial port
ser = serial.Serial('COM3', baud_rate, timeout=5)
sleepTime = 600000
shutdownTime = 86400000 #8.64e+7 = 24 hours
totalRunTime = 0

temperatureData = 'tempHumData.csv'
fields = ['timestamp','temperature','humidity','heatindex']
pathExists = (os.path.isfile(temperatureData))

if pathExists == False:
    # create a csv file
    with open('tempHumData.csv', 'w', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames = fields)
        writer.writeheader()

waiting(1)
while totalRunTime < (shutdownTime):
    # wait for new data, we know it will happen every 10 minutes
    waiting(sleepTime)
    totalRunTime += sleepTime
    # check data in the serial
    newValues = ser.readline().decode("utf-8")
    # check that newValues is not null
    if newValues is not None:
        # split the data into a dictionary
        splitValues = newValues.split(',')
        # check that we recieved and split into 3 values
        if len(splitValues) == 3:
            # prepare data for writing to csv
            newData = [[getTimeStamp(), splitValues[0], splitValues[1], splitValues[2]]]
            #print("{0}: Temp: {1}, Hum: {2}, HeatIndex: {3}".format(getTimeStamp(), splitValues[0], splitValues[1], splitValues[2]))
            # add data to csv file
            with open(temperatureData, 'a', newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerows(newData)
    

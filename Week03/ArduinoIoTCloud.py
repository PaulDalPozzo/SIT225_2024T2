#  Paul Dal Pozzo
#  s214527809
#  SIT225 - Data Capture Technologies
#  Week 03
#  Task 3.1P

import sys
import traceback
from arduino_iot_cloud import ArduinoCloudClient
import asyncio
import time
import csv
import os.path
from datetime import datetime

DEVICE_ID = b"fe409287-52b1-4db8-a582-214410f61c25"
SECRET_KEY = b"WTI219F0gt0iHRxbWOawBu8g3"

xAxis = float(1)
yAxis = float(1)
zAxis = float(1)

def get_time_stamp():
    now = datetime.now()        # now stores current time
    timeStamp = now.timestamp() # timeStamp stores timestamp of current time
    return timeStamp

# Callback functions on change event.
def on_x_changed(client, value):
    global xAxis
    xAxis = value
    #print(f"X: {value}, {xAxis}")
    save_changed_values()

def on_y_changed(client, value):
    global yAxis
    yAxis = value
    #print(f"Y: {value}, {yAxis}")
    save_changed_values()

def on_z_changed(client, value):
    global zAxis
    zAxis = value
    #print(f"Z: {value}, {zAxis}")
    save_changed_values()


def save_changed_values():
    global xAxis
    global yAxis
    global zAxis
    # prepare data for writing to csv
    timeStamp = get_time_stamp()
    newData = [[timeStamp, xAxis, yAxis, zAxis]]
    #newData = [timeStamp, xAxis, yAxis, zAxis]
    #print("{0}: X Axis: {1}, Y Axis: {2}, Z Axis: {3}".format(timeStamp, xAxis, yAxis, zAxis))
    print(f"{timeStamp}: X: {xAxis}, Y: {yAxis}, Z: {zAxis}")
    # add data to csv file
    with open(accelerometerData, 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(newData)


def main():
    print("Connect to Client")

    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)

    client.register("x_ax", value=None, on_write=on_x_changed)
    client.register("y_ax", value=None, on_write=on_y_changed)
    client.register("z_ax", value=None, on_write=on_z_changed)

    # start cloud client
    client.start()

#    accelerometerData = 'accelerometerData.csv'
#    fields = ['timestamp','x_axis','y_axis','z_axis']
#    pathExists = (os.path.isfile(accelerometerData))
    
#    if pathExists == False:
        # create a csv file
#        with open('accelerometerData.csv', 'w', newline='') as csvFile:
#            writer = csv.DictWriter(csvFile, fieldnames = fields)
#            writer.writeheader()
#    save_changed_values()


if __name__ == "__main__":
    try:
        accelerometerData = 'accelerometerData.csv'
        fields = ['timestamp','x_axis','y_axis','z_axis']
        pathExists = (os.path.isfile(accelerometerData))
        
        if pathExists == False:
            # create a csv file
            with open('accelerometerData.csv', 'w', newline='') as csvFile:
                writer = csv.DictWriter(csvFile, fieldnames = fields)
                writer.writeheader()
        main()  # main function which runs in an internal infinite loop
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_type, file=print)
#  Paul Dal Pozzo
#  s214527809
#  SIT225 - Data Capture Technologies
#  Week 05
#  Task 5.1P

student_id = "s214527809"
student_first_last_name = "Paul Dal Pozzo"

import sys
import traceback
import os.path
import firebase_admin
from firebase_admin import db
from datetime import datetime
from datetime import datetime
from arduino_iot_cloud import ArduinoCloudClient

DEVICE_ID = b"fe409287-52b1-4db8-a582-214410f61c25"
SECRET_KEY = b"WTI219F0gt0iHRxbWOawBu8g3"

xAxis: float = 1
yAxis: float = 1
zAxis: float = 1

GYROSCOPE_JSON: str = 'GyroscopeData.json'
GYROSCOPE_CSV: str = 'GyroscopeData.csv'
FIELDS: list[str] = ['timestamp','x_axis','y_axis','z_axis']
FIREBASE_CREDENTIALS_FILE: str = 'myfirstfirebase-a11cc-firebase-adminsdk-gnekq-04fb6ad8e3.json'
DATABASE_URL = 'https://myfirstfirebase-a11cc-default-rtdb.firebaseio.com/'


def get_time_stamp() -> datetime:
    # now stores current time
    now: datetime = datetime.now()
    # timeStamp stores timestamp of current time
    timeStamp: datetime = now.timestamp()
    return timeStamp

def send_to_firebase():
    timeStamp: datetime = get_time_stamp()
    # for testing purposes
    print(f"{timeStamp}: X: {xAxis}, Y: {yAxis}, Z: {zAxis}") 
    # prepare data for sending to Firebase
    newData = {
        "timestamp": timeStamp, 
        "x_axis": xAxis, 
        "y_axis": yAxis, 
        "z_axis": zAxis
    }

    ref = db.reference("/Gyroscope")
    ref.push().update(newData)

# Callback functions on change event.
def on_x_changed(client, value: float) -> None:
    global xAxis
    xAxis = value
    send_to_firebase()

def on_y_changed(client, value: float) -> None:
    global yAxis
    yAxis = value
    send_to_firebase()

def on_z_changed(client, value: float) -> None:
    global zAxis
    zAxis = value
    send_to_firebase()

def connect_to_firebase() -> None:
    print("Connect to Firebase")
    # checking that Firebase data file exists
    if (os.path.isfile(FIREBASE_CREDENTIALS_FILE)) :
        cred_obj = firebase_admin.credentials.Certificate(
            FIREBASE_CREDENTIALS_FILE
        )
    # initialize connection
    default_app = firebase_admin.initialize_app(cred_obj, {
        'databaseURL':DATABASE_URL
        })
    
    # get reference to Firebase Data
    # create a folder for Gyroscope
    ref = db.reference("/")
    ref.set({
        "Gyroscope": -1
    })

def connect_to_arduino() ->  None:
    print("Connect to Client")
    # register all axis value changes for on cloud sync
    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)
    client.register("x_ax", value=None, on_write=on_x_changed)
    client.register("y_ax", value=None, on_write=on_y_changed)
    client.register("z_ax", value=None, on_write=on_z_changed)
    # start cloud client
    client.start()

def main():
    connect_to_firebase() 
    connect_to_arduino()

if __name__ == "__main__":
    try:
        main()  # main function which runs in an internal infinite loop
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_type, file=print)







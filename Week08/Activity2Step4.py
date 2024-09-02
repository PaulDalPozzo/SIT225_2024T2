import sys
import traceback
from arduino_iot_cloud import ArduinoCloudClient
import csv
import os.path
from datetime import datetime

DEVICE_ID: str = b"a2f8b6ce-747a-47f1-bd04-56d152ed6469"
SECRET_KEY: str = b"UDfrFc6GZbIPJPhU?Ggwplyzy"

# CSV file names
MERGE_CSV: str = 'Python_Accelerometer.csv'

xAxis: float = 0
yAxis: float = 0
zAxis: float = 0

# returns time stamp of now in datetime
def get_time_stamp() -> datetime:
    now: datetime = datetime.now()        # now stores current time
    timeStamp: datetime = now.timestamp() # timeStamp stores timestamp of current time
    return timeStamp

# checks if file exists and creates it
def check_file_exist(filename: str, fields: list[str]) -> None:
    # check if file path exists
    pathExists: bool = (os.path.isfile(filename))
    # if it does not exist
    if pathExists == False:
        # create a csv file
        with open(filename, 'w', newline='') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames = fields)
            writer.writeheader()

# prepares values to be saved, and saves to a csv file
def save_changed_values(value: float, filename: str) -> None:
    global xAxis
    global yAxis
    global zAxis
    # prepare data for writing to csv
    timeStamp: datetime = get_time_stamp()
    newData = [[timeStamp, xAxis, yAxis, zAxis]]
    print(f"{timeStamp}: X: {xAxis}, Y: {yAxis}, Z: {zAxis}")
    # add data to csv file
    with open(filename, 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(newData)

# callback functions for each axes
def on_x_changed(client, value: float) -> None:
    global xAxis
    xAxis = value
    save_changed_values(value, MERGE_CSV)

def on_y_changed(client, value: float) -> None:
    global yAxis
    yAxis = value
    save_changed_values(value, MERGE_CSV)

def on_z_changed(client, value: float) -> None:
    global zAxis
    zAxis = value
    save_changed_values(value, MERGE_CSV)

# main
# connects to Arduino Cloud and registers callbacks
def main() -> None:
    print("Connect to Client")

    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)
    client.register("x_axis", value=None, on_write=on_x_changed)
    client.register("y_axis", value=None, on_write=on_y_changed)
    client.register("z_axis", value=None, on_write=on_z_changed)
    # start cloud client
    client.start()

if __name__ == "__main__":
    try:
        # create field header names
        fields = ['timestamp','x', 'y', 'z']
        check_file_exist(MERGE_CSV, fields)
        main()  # main function which runs in an internal infinite loop
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_type, file=print)
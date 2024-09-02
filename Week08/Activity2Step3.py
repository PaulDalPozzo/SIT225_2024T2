import sys
import traceback
from arduino_iot_cloud import ArduinoCloudClient
import csv
import os.path
from datetime import datetime

DEVICE_ID: str = b"a2f8b6ce-747a-47f1-bd04-56d152ed6469"
SECRET_KEY: str = b"UDfrFc6GZbIPJPhU?Ggwplyzy"

# CSV file names
X_CSV: str = 'Python_Accelerometer_X.csv'
Y_CSV: str = 'Python_Accelerometer_Y.csv'
Z_CSV: str = 'Python_Accelerometer_Z.csv'

# returns time stamp of now in datetime
def get_time_stamp() -> datetime:
    now: datetime = datetime.now()        # now stores current time
    timeStamp: datetime = now.timestamp() # timeStamp stores timestamp of current time
    return timeStamp

# checks if file exists and creates it
def check_file_exist(filename: str) -> None:
    # check if file path exists
    pathExists: bool = (os.path.isfile(filename))
    # if it does not exist
    if pathExists == False:
        # create field header names
        fields = ['timestamp','data-value']
        # create a csv file
        with open(filename, 'w', newline='') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames = fields)
            writer.writeheader()

# prepares values to be saved, and saves to a csv file
def save_changed_values(value: float, filename: str) -> None:
    # prepare data for writing to csv
    timeStamp: datetime = get_time_stamp()
    newData = [[timeStamp, value]]
    # add data to csv file
    with open(filename, 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(newData)

# callback functions for each axes
def on_x_changed(client, value: float) -> None:
    print('New X value: {0}'.format(value))
    save_changed_values(value, X_CSV)

def on_y_changed(client, value: float) -> None:
    print('New Y value: {0}'.format(value))
    save_changed_values(value, Y_CSV)

def on_z_changed(client, value: float) -> None:
    print('New Z value: {0}'.format(value))
    save_changed_values(value, Z_CSV)

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
        check_file_exist(X_CSV) 
        check_file_exist(Y_CSV) 
        check_file_exist(Z_CSV) 
        main()  # main function which runs in an internal infinite loop
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_type, file=print)
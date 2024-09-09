# Fill in student ID and name
student_id = "s214527809"
student_first_last_name = "Paul Dal Pozzo"
print(student_id, student_first_last_name)

#imports
import sys
import traceback
import threading
from arduino_iot_cloud import ArduinoCloudClient
import csv
import os.path
from datetime import datetime
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Arduino Details
DEVICE_ID: str = b"a2f8b6ce-747a-47f1-bd04-56d152ed6469"
SECRET_KEY: str = b"UDfrFc6GZbIPJPhU?Ggwplyzy"

# CSV file names
FOLDER_CSV: str = 'csv'
PREFIX_CSV: str = 'csv/Task81P_'
SUFFIX_CSV: str = '.csv'
# HTML file names
FOLDER_HTML: str = 'html'
PREFIX_HTML: str = 'html/Task81P_'
SUFFIX_HTML: str = '.html'
# CONSTANTS
BUFFER: int = 20
SAMPLE_SIZE: int = 800

# gathered from readings
xBuffer: list[float] = [0] 
yBuffer: list[float] = [0]
zBuffer: list[float] = [0]
# list of samples to plot
xPlot: list[float] = [0] 
yPlot: list[float] = [0]
zPlot: list[float] = [0]
# list to save to csv
csvList: list[float, float, float] = []
# bool to check if first 1000 entries have been ploted
first_plot: bool = False
# set up figure
graph = {}
# Initialize the app
app = Dash()

# set up dataframe
df = pd.DataFrame({'x': xPlot})
df['y'] = yPlot
df['z'] = zPlot

def get_time_stamp() -> str:
    now: datetime = datetime.now()
    # get string of time in format H:M:S
    timeStamp: str = now.strftime('%H-%M-%S')
    return timeStamp

def check_csv_exist(folder: str, filename: str, fields: list[str]) -> None:
    # if folder does not exist
    if not os.path.exists(folder):
        os.mkdir(folder)

    # if file does not exist
    if not os.path.isfile(filename):
        # create a csv file
        with open(filename, 'w', newline='') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames = fields)
            writer.writeheader()

def save_to_csv(filename: str) -> None:
    # leave if csvList has no entries
    if (len(csvList) == 0): 
        return
    print("SAVE TO CSV")
    # add data to csv file
    with open(filename, 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        # only write the buffer amount of entries
        for item in csvList:
            writer.writerow(item)

def prepare_data_for_save(timeStamp: str) -> None:
    # create filename with timestamp in it
    filename: str = PREFIX_CSV + timeStamp + SUFFIX_CSV
    # create field header names
    fields = ['x', 'y', 'z']
    # check file exists or create it
    check_csv_exist(FOLDER_CSV, filename, fields)
    # save data to csv
    save_to_csv(filename)

def check_html_exist(folder: str, filename: str) -> None:
    # if folder does not exist
    if not os.path.exists(folder):
        os.mkdir(folder)

    # if file does not exist
    if not os.path.isfile(filename):
        print("SAVE TO HTML")
        # create a html file
        graph.write_html(filename)

def save_plot(timeStamp: str):
    # create filename with timestamp in it
    filename: str = PREFIX_HTML + timeStamp + SUFFIX_HTML
    # check file exists or create it
    check_html_exist(FOLDER_HTML, filename)

def add_buffer_to_csvList(toList: list, x: list, y: list, z: list, buffer: int) -> None:
    # make sure x y z lists lengths are at least equal to the buffer
    if (len(x) < buffer or len(y) < buffer or len(z)  < buffer):
        return
    # add new entries from the buffer
    i: int = 0
    while (i < buffer):
        toList.append([x[i], y[i], z[i]])
        i += 1

def remove_first_entries(toShorten: list, buffer: int) -> None:
    del toShorten[:buffer]

def add_buffer_to_list(toList: list, fromList: list, buffer: int) -> None:
    # add new entries from the buffer
    i: int = 0
    while (i < buffer):
        toList.append(fromList[i])
        i += 1

def add_to_lists(change: int) -> None:
    # add new data to lists to plot
    add_buffer_to_list(xPlot, xBuffer, change)
    add_buffer_to_list(yPlot, yBuffer, change)
    add_buffer_to_list(zPlot, zBuffer, change)
    add_buffer_to_csvList(csvList, xBuffer, yBuffer, zBuffer, change)

def remove_from_lists(change: int) -> None:
    # remove oldest entries from plot lists
    if (len(xPlot) >= change):
        remove_first_entries(xPlot, change)
    else:
        remove_first_entries(xPlot, len(xPlot))
    if (len(yPlot) >= change):
        remove_first_entries(yPlot, change)
    else:
        remove_first_entries(yPlot, len(yPlot))
    if (len(zPlot) >= change):
        remove_first_entries(zPlot, change)
    else:
        remove_first_entries(zPlot, len(zPlot))
    # update csv list for saving
    if (len(csvList) >= change):
        remove_first_entries(csvList, change)
    # remove first entries from buffer lists
    remove_first_entries(xBuffer, change)
    remove_first_entries(yBuffer, change)
    remove_first_entries(zBuffer, change)

def update_plot():
    newData = pd.DataFrame({'x':xPlot})
    newData['y'] = yPlot
    newData['z'] = zPlot
    global df
    df = newData

def check_hit_buffer() -> None:
    global first_plot
    if (first_plot == False):
        if (len(xBuffer) >= SAMPLE_SIZE and len(yBuffer) >= SAMPLE_SIZE and len(zBuffer) >= SAMPLE_SIZE):
            add_to_lists(SAMPLE_SIZE)
            update_plot()
            first_plot = True
        # stop access to below until the sample size is reached
        return

    # if all buffer lists have a length greater than the buffer amount
    if (len(xBuffer) >= BUFFER and len(yBuffer) >= BUFFER and len(zBuffer) >= BUFFER):
        timeStamp: str = get_time_stamp()
        # save plot
        save_plot(timeStamp)
        # save csv
        prepare_data_for_save(timeStamp)
        # update all lists
        add_to_lists(BUFFER)
        remove_from_lists(BUFFER)
        # update plotly dash
        update_plot()

def on_x_changed(client, value: float) -> None:
    xBuffer.append(value)

def on_y_changed(client, value: float) -> None:
    yBuffer.append(value)

def on_z_changed(client, value: float) -> None:
    zBuffer.append(value)
    #check_hit_buffer()

# App layout
app.layout = html.Div([
    html.H1(children='Task 8.1P - {0} - {1}'.format(student_id, student_first_last_name)),
    html.Hr(),
    html.Div([
        # drop down menu for graph types
        html.Label('Graph Type'),
        dcc.Dropdown([
            'Bar',
            'Grouped Bar', 
            'Line', 
            'Scatter', 
            'Cumulative Distribution',
            'Histogram Average',
            'Violin',
            'Box'
        ], 'Line', multi=False, id='graph-type'),
        html.Br(),
        ],
        style={'width': '25%', 'display': 'inline-block'}
    ),
    html.Hr(),
    html.Div([
        dcc.Graph(figure={}, id='graph-display'),
        dcc.Interval( id='interval-component', interval=1*100, n_intervals=0)
    ],
        style={'padding-left': '50px'}
    ),
    html.Hr()
], 
style={'background-color': 'rgb(200, 200, 200)'}
)

def make_figure_for_display(data, graph_type):
    WIDTH: int = 1500
    HEIGHT: int = 500
    fig = {}
    variable_chosen = ['x', 'y', 'z']
    # LINE GRAPH
    if graph_type == 'Line':
        fig = px.line(
            data,
            title=graph_type,
            x=data.index, 
            y=variable_chosen,
            width=WIDTH, 
            height=HEIGHT,
            markers=True
        )
    # SCATTER GRAPH
    if graph_type == 'Scatter':
        fig = px.scatter(
            data,
            title=graph_type,
            x=data.index, 
            y=variable_chosen,
            width=WIDTH, 
            height=HEIGHT
        )
    # BAR GRAPH
    if graph_type == 'Bar':
        fig = px.bar(
            data,
            title=graph_type,
            x=data.index, 
            y=variable_chosen,
            width=WIDTH, 
            height=HEIGHT
        )
    # GROUPED BAR GRAPH
    if graph_type == 'Grouped Bar':
        fig = px.bar(
            data,
            title=graph_type,
            x=data.index, 
            y=variable_chosen,
            width=WIDTH, 
            height=HEIGHT,
            barmode='group'
        )
    # HISTOGRAM AVERAGE GRAPH
    if graph_type == 'Histogram Average':
        fig = px.histogram(
            data,
            title=graph_type,
            x=data.index, 
            y=variable_chosen,
            width=WIDTH, 
            height=HEIGHT,
            histfunc='avg'
        )
    # VIOLIN GRAPH
    if graph_type == 'Violin':
        fig = px.violin(
            data,
            title=graph_type,
            y=variable_chosen,
            width=WIDTH, 
            height=HEIGHT
        )
    # ECDF GRAPH
    if graph_type == 'Cumulative Distribution':
        fig = px.ecdf(
            data,
            title=graph_type,
            x=variable_chosen,
            width=WIDTH, 
            height=HEIGHT
        )
    # BOX GRAPH
    if graph_type == 'Box':
        fig = px.box(
            data,
            title=graph_type,
            y=variable_chosen,
            points='all',
            width=WIDTH, 
            height=HEIGHT
        )
    fig.update_layout(plot_bgcolor = "rgb(250,250,250)", paper_bgcolor = "rgb(200, 200, 200)")
    global graph
    graph = fig
    return fig

@callback(
    Output(component_id='graph-display', component_property='figure'),
    Input(component_id='graph-type', component_property='value'),
    Input(component_id='interval-component', component_property='n_intervals')
)
def update_graph(graph_type_chosen, interval_count):
    check_hit_buffer()
    global df
    data = df
    return make_figure_for_display(data, graph_type_chosen)

def run_arduino() -> None:
    print("Connect to Client")
    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)
    client.register("py_x", value=None, on_write=on_x_changed)
    client.register("py_y", value=None, on_write=on_y_changed)
    client.register("py_z", value=None, on_write=on_z_changed)
    # start cloud client
    client.start()

if __name__ == "__main__":
    try:
        thread_arduino = threading.Thread(target=run_arduino)
        thread_arduino.start()
        thread_dash = threading.Thread(app.run(debug=True))
        thread_dash.start()
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_type, file=print)
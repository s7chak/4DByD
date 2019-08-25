#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, jsonify, session, request, \
	copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
	close_room, rooms, disconnect
from forms import ErrorSearchForm
import time, re, json, csv, requests, os
import subprocess
from datetime import datetime, date

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
filename = 'test.txt'
errorcount = 0
log_list = []
api_key = "02e4e46503b043e2bf441dc3108e22b4"


def flatten(arr):
    print(arr)
    if isinstance(arr, list):
        if len(arr) == 0:
            return None
        elif len(arr) == 1:
            return arr[0]
    return arr


def background_thread(filename):
    print(filename)
    lines = ''
    l2 = 'none'
    thefile = open(filename, 'r')
    thefile.seek(0, 2)
    while True:
        lines = ''
        print("reading....")
        line = thefile.readline()
        if not line:
            time.sleep(1)
            continue
        elif 'Got exception' in line:
            print("-------------Found Error!")
            lines += line

            while 'Error:' not in line:
                line = thefile.readline()
                lines += line
            line = thefile.readline()
            print(lines)

            socketio.emit('err', errorLog(lines), namespace='/test')

            print(log_list)

            with open('data2.csv', 'w') as output_file:
                dict_writer = csv.DictWriter(output_file,
                                             fieldnames=["ID", "Time", "ErrorType", "ErrorMessage", "File-Line",
                                                         "ProjectName"])
                dict_writer.writeheader()
                dict_writer.writerows(log_list)

# Generate Json String (The return is Json String, therefore index will be weird)

def errorLog(i):
    ErrorLog = []
    print("-------------JSONifying Error")
    # Initialize
    x = 0
    global errorcount
    ErrorLog = {}
    # for i in Data:
    # Timestamp
    Time = flatten(re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', i))
    print(Time)
    # Error Type
    ErrorType = flatten(re.findall(r'\n(\S+Error)', i))
    # Error Message
    ErrorMsg = flatten(re.findall(r'Error:\s(.*)', i))
    # File Location and File Name
    File = re.findall(r'File \"(.*)\"', i)
    # Error line of code
    Line = flatten(re.findall(r'line (\d+)', i))
    # Create Dictionary that records the trackback sequence and files
    Dict = {}
    for j in range(len(File)):
        ErrorDest = {}
        # Create Tuple with matched File Name and Error Line
        ErrorDest = {"File": flatten(File[j]), "Line": flatten(Line[j])}
        # Match sequence with Tuple
        Dict[j] = ErrorDest
    x = x + 1
    today = datetime.now().strftime("%Y-%m-%d")
    date = datetime.strptime(Time, "%Y-%m-%d %H:%M:%S")
    datestring = date.strftime("%Y-%m-%d")
    print(today)
    print(date)
    if today == datestring:
        print("ErrCount:" + str(errorcount))
        errorcount += 1
    else:
        errorcount = 0
    ProjectName = datestring + "_" + str(errorcount)
    ErrorLog = {"ID": errorcount, "Time": Time, "ErrorType": ErrorType, "ErrorMessage": ErrorMsg, "File-Line": Dict,
                "ProjectName": ProjectName}
    log_list.append(ErrorLog)

    return json.dumps(ErrorLog)

@app.route('/')
def index():
	return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('setfilename', namespace='/test')
def setfilename():
	global filename
	filename = '../jupyter.log'
	socketio.emit('msg', jsonify('success'), namespace='/test')


@socketio.on('openfile', namespace='/test')
def openfilesocket(message):
    print("------OPEN FILE------")
    jsonobject = message
    fileLine = jsonobject['File-Line']
    print("------OPEN FILE------")
    for key, value in fileLine.items():
        print("------OPEN FILE------")
        File = value['File']
        Line = value['Line']
        if '<ipython' not in File:
            openfile(File, Line)


def openfile(File, Line=""):
	Path = File + ":" + Line
	subprocess.Popen(['code', '-g', Path])


@app.route("/search", methods=['GET', 'POST'])
def errorsearch():
    form = ErrorSearchForm()
    if form.validate_on_submit():
        print(searchFile(form.filename.data, form.date.data))
    return render_template("search.html", title="Search Error", form=form)


@socketio.on('connect', namespace='/test')
def test_connect():
	global thread
	with thread_lock:
		if thread is None:
			filename = '../jupyter.log'
			errorcount = 0
			print("ErrCount:" + str(errorcount))
			thread = socketio.start_background_task(background_thread, filename)
	emit('my_response', {'data': 'Connected', 'count': 0})

# @app.route("/create", methods=['GET', 'POST'])
def createFolder():

    today = date.today()
    mmddyy = today.strftime("%m-%d-%y")
    folderName = mmddyy + ""
    metaDataJson = { "objects": [{"properties": {"enaio:objectTypeId" : {"value" : "userDirectory"}, "name": {"value": folderName}}}] }

    jsonPath = r'json/metadataparent.json'
    fd = os.open(jsonPath, os.O_RDWR|os.O_CREAT)
    with open(jsonPath, 'w') as fd:
        fd.write(json.dumps(metaDataJson))

    headerDict = {}
    baseUrl = 'https' + '://' + 'api.yuuvis.io'

    header_name = 'Content-Type'
    # headerDict['Content-Type'] = 'multipart_form_data, application/x-www-form-urlencoded'
    # headerDict['Content-Type'] = 'application/json'

    header_name = 'Ocp-Apim-Subscription-Key'
    headerDict['Ocp-Apim-Subscription-Key'] = api_key

    session = requests.Session()

    multipart_form_data = {
        'data' :('data.json', open(jsonPath, 'rb'), 'application/json')
    }

    print("resp:")
    response = session.post(str(baseUrl + '/dms/objects'), files=multipart_form_data, headers=headerDict)
    print(response.json())
    addFile(folderName)
    # return (response.content)


# @app.route("/<folder>/add", methods=['GET', 'POST'])
def addFile(folder):

    queryJson = {"query": { "statement": "SELECT * FROM enaio:object WHERE CONTAINS ('{}')".format(folder), "skipCount": 0, "maxItems": 50}}

    metaDataJson = { "objects": [{"properties": {"enaio:objectTypeId" : {"value" : "documentType1"}, "name": {"value": filename}, "enaio:parentId": {"value": "8b3b452c-07d2-489a-8b79-91d46f802bac"} }, "contentStreams": [{"cid": "cid_63apple"}] }] }


    jsonPath = "json/metadatachild.json"
    contentPath = "content/error8.txt" ## this is the error file you are trying to upload

    fd = os.open(jsonPath, os.O_RDWR | os.O_CREAT)
    with open(jsonPath, 'w') as fd:
        fd.write(json.dumps(metaDataJson))

    headerDict = {}
    baseUrl = 'https' + '://' + 'api.yuuvis.io'

    header_name = 'Content-Type'

    header_name = 'Ocp-Apim-Subscription-Key'
    headerDict['Ocp-Apim-Subscription-Key'] = api_key

    session = requests.Session()

    multipart_form_data = {
        'data' :('data.json', open(jsonPath, 'rb'), 'application/json'),
        'cid_63apple' : ('content.pdf', open(contentPath, 'rb'), 'application/pdf')
    }

    print(type(multipart_form_data))
    #print("--searchResp")
    #searchResp = session.post(str(baseUrl + '/dms/objects/search'), json=queryJson, headers=headerDict)
    #print(searchResp.json())

    response = session.post(str(baseUrl + '/dms/objects'), files=multipart_form_data, headers=headerDict)
    print("--resp--")
    print(response.json())
    return (response.content)

# @app.route("/searchFile", methods=['GET','POST'])
def searchFile():
    fileName = request.args.get('name')
    date = request.args.get('date')


    fileName = request.args.get('name')
    date = request.args.get('date')

    queryJson = {"query": { "statement": "SELECT * FROM enaio:object WHERE CONTAINS ('{}') AND enaio:creationDate = '{}'".format(fileName,date), "skipCount": 0, "maxItems": 50}}
    print(queryJson)

    headerDict = {}
    baseUrl = 'https' + '://' + 'api.yuuvis.io'

    header_name = 'Content-Type'

    header_name = 'Ocp-Apim-Subscription-Key'
    headerDict['Ocp-Apim-Subscription-Key'] = api_key

    session = requests.Session()

    multipart_form_data = {
        'data': ('data.json', queryJson, 'application/json')
    }

    print(type(multipart_form_data))
    print("resp")
    response = session.post(str(baseUrl + '/dms/objects/search'), json=queryJson, headers=headerDict)
    print(response.json())
    return (response.content)

if __name__ == '__main__':
	socketio.run(app, debug=True)

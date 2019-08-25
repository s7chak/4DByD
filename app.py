#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

import time, re, json
import subprocess
from datetime import datetime

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
filename='test.txt'
errorcount=0
log_list=[]
​
def flatten(arr):
    print(arr)
    if isinstance(arr, list):
        if len(arr) == 0:
            return None
        elif len(arr) == 1:
            return arr[0]
    return arr
​
def background_thread(filename):
    
    print(filename)
    lines=''
    l2='none'
    thefile = open(filename,'r')
    thefile.seek(0,2)
    while True:
        lines=''
        print("reading....")
        line = thefile.readline()
        if not line:
            time.sleep(1)
            continue
        elif 'Got exception' in line:
            print("-------------Found Error!")
            lines+=line
            while 'Error:' not in line:
                line=thefile.readline()
                lines+=line
            line=thefile.readline()
            print(lines)
            print(log_list)
​
            with open('data2.csv', 'w') as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=["ID","Time","ErrorType","ErrorMessage","File-Line","ProjectName"])
                dict_writer.writeheader()
                dict_writer.writerows(log_list)
​
​
            socketio.emit('err', errorLog(lines), namespace='/test')
​
        
​
​
#Generate Json String (The return is Json String, therefore index will be weird)
    
def errorLog(i):
    ErrorLog = []
    print("-------------JSONifying Error")
    #Initialize
    x=0
    global errorcount
    ErrorLog = {}
    # for i in Data:
    #Timestamp
    Time = flatten(re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',i))
    print(Time)
    #Error Type
    ErrorType = flatten(re.findall(r'\n(\S+Error)', i))
    #Error Message
    ErrorMsg = flatten(re.findall(r'Error:\s(.*)', i))
    #File Location and File Name
    File = re.findall(r'File \"(.*)\"', i)
    #Error line of code
    Line = flatten(re.findall(r'line (\d+)', i))
    #Create Dictionary that records the trackback sequence and files
    Dict = {}
    for j in range(len(File)):
        ErrorDest={}
        #Create Tuple with matched File Name and Error Line 
        ErrorDest = {"File":flatten(File[j]),"Line":flatten(Line[j])}
        #Match sequence with Tuple
        Dict[j]=ErrorDest
    x=x+1
    today = datetime.now().strftime("%Y-%m-%d")
    date=datetime.strptime(Time, "%Y-%m-%d %H:%M:%S")
    datestring=date.strftime("%Y-%m-%d")
    print(today)
    print(date)
    if today == datestring:       
        print("ErrCount:"+str(errorcount))
        errorcount+=1
    else:
        errorcount=0
    ProjectName = datestring+"_"+str(errorcount)
    ErrorLog = {"ID":errorcount,"Time":Time,"ErrorType":ErrorType,"ErrorMessage":ErrorMsg,"File-Line":Dict, "ProjectName":ProjectName}
    log_list.append(ErrorLog)
    
    return json.dumps(ErrorLog)
​

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('setfilename', namespace='/test')
def setfilename():
    global filename
    filename='../jupyter.log'
    socketio.emit('msg', jsonify('success'), namespace='/test')





@socketio.on('openfile', namespace='/test')
def openfilesocket(message):
    print("------OPEN FILE------")
    jsonobject = message
    fileLine = jsonobject['File-Line']
    for key, value in fileLine.items():
        File=value['File']
        Line=value['Line']
        if '<ipython' not in File:
            openfile(File,Line)


def openfile(File,Line=""):
    Path = File+":"+Line
    subprocess.Popen(['code', '-g', Path])


@app.route("/search", methods=['GET','POST'])
def zipsearch():
    form = ErrorSearchForm()
    if form.validate_on_submit():
        func = MainFunctions()
        vsworkspace = func.get_vsfile_on_search(form.filename.data)

    return render_template("search.html", title="Search Error", form=form)



@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
          filename='../jupyter.log'
          errorcount=0
          print("ErrCount:"+str(errorcount))
          thread = socketio.start_background_task(background_thread, filename)
    emit('my_response', {'data': 'Connected', 'count': 0})



if __name__ == '__main__':
    socketio.run(app, debug=True)

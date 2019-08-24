#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

import time, re, json
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


def background_thread(filename):
    lines=[]
    l2='none'
    thefile = open(filename,'r')
    thefile.seek(0,2)
    errcount = 0
    while True:
        print("reading....")
        line = thefile.readline()
        if not line:
            time.sleep(1)
            continue
        elif ('Traceback' in line):
            print("-------------Found Error!")
            lines+=line
            while 'Error:' not in line:
                line=thefile.readline()
                lines+=line
            print(str(errorLog(lines)))



#Generate Json String (The return is Json String, therefore index will be weird)
def errorLog(Data):
    x=0
    ErrorLog = []
    print("-------------JSONifying Error")
    #For each splitted segment
    for i in Data:
        #Timestamp
        Time = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',i)
        #Error Type
        ErrorType = re.findall(r'\n(\S+Error)', i)
        #Error Message
        ErrorMsg = re.findall(r'Error:\s(.*)', i)
        #File Location and File Name
        File = re.findall(r'File \"(.*)\"', i)
        #Error line of code
        Line = re.findall(r'line (\d+)', i)
        #Create Dictionary that records the trackback sequence and files
        Dict = {}
        for j in range(len(File)):
            #Create Tuple with matched File Name and Error Line 
            ErrorDest = (File[j],Line[j])
            #Match sequence with Tuple
            Dict[j]=ErrorDest
        ErrorLog.append([x,Time,ErrorType,ErrorMsg,Dict])
        x=x+1
    return json.dumps(ErrorLog)


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)



@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
          filename='../jupyter.log'
          thread = socketio.start_background_task(background_thread, filename)
    emit('my_response', {'data': 'Connected', 'count': 0})



if __name__ == '__main__':
    socketio.run(app, debug=True)

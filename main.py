# [START gae_python37_cloudsql_mysql]
import os

from flask import Flask, render_template, url_for, redirect, flash, jsonify, request, session, json
# from func.mainfunctions import MainFunctions
# from func.commonfunctions import CommonFunctions
from func import Functions as mfunc
from datetime import datetime
import time, logging
from threading import Thread
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config['SECRET_KEY'] = '294d86e9fd5e4b179261796459238211'
socketio = SocketIO(app)


# Routes for Android App
@app.route("/")
def home():
    try:
        filename='../jupyter.log'
        t1 = Thread(target=read_logs, args=(filename,))
        t1.start()
    except:
        print("Error: unable to start thread")
    return render_template("welcome.html")

    


def read_logs(filename):
        lines=[]
        l2='none'
        thefile = open(filename,'r')
        thefile.seek(0,2)
        while True:
            print("reading....")
            line = thefile.readline()
            l2=line
            if not line:
                time.sleep(1)
                continue
            elif ('Traceback' in line):
                lines+=l2
                while 'Error:' not in l2:
                    l2=thefile.readline()
                    lines+=l2
                    print("Printing from Flask: "+l2)
                errors(lines)


@socketio.on('error event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})

@app.route("/ping")
def ping():
    return "pong"


@app.route("/errors")
def errors(lines):

    render_template("")
            



if __name__ == '__main__':
    socketio.run(app)

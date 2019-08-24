# [START gae_python37_cloudsql_mysql]
import os

from flask import Flask, render_template, url_for, redirect, flash, jsonify, request, session, json
from forms import SignUpForm, LoginForm, ZipSearchForm, VenueDateForm, StartEventForm, DateSearchForm
import pymysql
# from func.mainfunctions import MainFunctions
# from func.commonfunctions import CommonFunctions
from func import Functions as mfunc
from datetime import datetime
import time


db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)
app.config['SECRET_KEY'] = '294d86e9fd5e4b179261796459238211'


# Routes for Android App
@app.route("/")
def home():
    thefile = open('../jupyter.log','r')
    thefile.seek(0,2)
    lines=[]
    l2='none'
    while True:
        # print("reading....")
        line = thefile.readline()
        l2=line
        if not line:
            time.sleep(1)
            continue
        elif ('Traceback' in line):
            print("Printing from Flask: "+line)
            while 'Error:' not in l2:
                l2=thefile.readline()
                print("Printing from Flask: "+l2)
            
            



if __name__ == '__main__':
    
    app.run(host='127.0.0.1',port=8080,debug=True)

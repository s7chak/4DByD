# [START gae_python37_cloudsql_mysql]
import os

from flask import Flask, render_template, url_for, redirect, flash, jsonify, request, session, json
from forms import SignUpForm, LoginForm, ZipSearchForm, VenueDateForm, StartEventForm, DateSearchForm
import pymysql
from func.mainfunctions import MainFunctions
from func.commonfunctions import CommonFunctions
from datetime import datetime


db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)
app.config['SECRET_KEY'] = '294d86e9fd5e4b179261796459238269'


# Routes for Android App
# Routes for Android App
@app.route("/applogin/<username>/<password>", methods=['GET'])
def applogin(username, password):
    func = MainFunctions()
    userdata={}
    print(username)
    userdata['username']=username
    userdata['password']=password

    result = func.log_in(userdata)
    if(result[0] == 1):
        session['userid'] = result[3]
        print(str(session['userid'])+" set as signed in user")
        return jsonify(
            loggedin=result[0],
            adminstatus=result[1],
            status=result[2],
            userid=result[3]
        )
    else:
        return jsonify(loggedin=0)

@app.route("/appsignup", methods=['POST'])
def appsignup():

    json = request.get_json()
    if len(json['userName']) != 0:
        func = MainFunctions()
        userdata = {}
        userdata['username'] = json['userName']
        userdata['firstname'] = json['firstName']
        userdata['lastname'] = json['lastName']
        userdata['email'] = json['email']
        userdata['password'] = json['password']
        userdata['zipcode'] = json['zipCode']
        userdata['isadmin'] = "N"

        result = func.add_user(userdata)
        return jsonify(result=result)
    else:
        return jsonify(result=9)



@app.route("/appzipsearch/<zipcode>", methods=['GET'])
def appzipsearch(zipcode):
    func = MainFunctions()
    userdata={}
    print(zipcode)
    userdata['zipcode']=zipcode
    result = func.display_events_for_zipcode(zipcode)
    eventlist = list()
    for row in result:
        a = dict()
        a['eventname'] = row[0]
        datestring = row[1]
        dated=datetime.strftime(datestring, '%Y-%m-%d')
        a['eventdate'] = dated
        a['venue'] = row[2]
        a['starttime'] = row[3]
        a['endtime'] = row[4]
        a['eventid'] = row[5]
        a['spots'] = row[6]
        eventlist.append(a)

    s = json.dumps(eventlist)


    # s = jsonify(result=result)
    return s


@app.route("/appjoinevent/<eventid>/<userid>", methods=['GET'])
def  appjoinevent(eventid, userid):
    func = MainFunctions()
    print(userid+":"+eventid)
    result = func.user_joins_event(userid,eventid)
    print(result)
    return jsonify(message=result)

@app.route("/appgetvenues", methods=['GET'])
def appgetvenues():
    func = CommonFunctions()
    result = func.get_all_venues()
    venuelist = list()
    for row in result:
        a = dict()
        a['venueid'] = row[0]
        a['venuename'] = row[1]
        venuelist.append(a)
    s = json.dumps(venuelist)

    return s


@app.route("/appstartevent", methods=['POST'])
def appstartevent():
    json = request.get_json()
    mainfunc = MainFunctions()
    data={}
    data['venueid'] = json['venue']
    data['username'] = json['username']
    data['eventname'] = json['eventname']
    data['eventdesc'] = json['eventdesc']
    data['eventdate'] = json['eventdate']
    data['starttime'] = json['starttime']
    data['endtime'] = json['endtime']
    data['eventcapacity'] = json['eventcapacity']
    data['genderoption'] = 'C'
    result = mainfunc.start_event(data)

    a = dict()
    a['result'] = result[0]
    a['message'] = result[1]

    s = jsonify(a)

    return s


@app.route("/appjoinedgames/<userid>", methods=['GET'])
def appjoinedgames(userid):
    json = request.get_json()
    func = MainFunctions()
    data={}
    data['userid'] = userid
    result = func.events_joined_user_id_dict(userid)

    return jsonify(result[1])

@app.route("/info")
def info():
    return render_template("info.html", title="Information", admin=session['admin'])

@app.route("/about")
def about():
    return render_template("about.html", title="About", admin=session['admin'])

@app.route("/how-to")
def howto():
    return render_template("howto.html", title="How-To Guide", admin=session['admin'])

@app.route("/how-to-admin")
def howtoadmin():
    return render_template("howtoadmin.html", title="How-To Admin Guide", admin=session['admin'])


@app.route("/")
def welcome():
    return render_template("welcome.html", title="Home")

@app.route("/home")
def home():
    if 'username' in session:
        return render_template("home.html", admin=session['admin'])
    else:
        return redirect(url_for('login'))

@app.route("/admin")
def admin():
    if 'admin' in session:
        if session['admin'] == 'A':
            return render_template("admin.html")
        else:
            return "<h2>Sorry, you are not an admin user at Soccer Hours</h2>"
    else:
        return redirect(url_for('login'))

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        func = MainFunctions()
        userdata = {}
        userdetail = {}
        userdata['username'] = form.username.data
        userdata['password'] = form.password.data


        result = func.log_in(userdata)
        if result[0]==1:
                # request.session['username_sh']=userdata['username']
                # request.session['adminuser']=result[1]
                # request.session['userstatus']=result[2]
                print(result[1], result[2])
                if result[2]!='I':
                    session['userid']=result[3]
                    session['admin']=result[1]
                    session['username']=result[4]
                    print("Logged in : "+result[4])
                    if result[1]=='A':
                        userdetail['admin']=True
                    else:
                        userdetail['admin']=False
                else:
                    return "<h2 align='center'>Sorry, your account is in an Inactive state.<br> Please contact administrator to activate it.</h2><br><a href='home'>Home</a>"
                return redirect(url_for('home'))
        else:
            return ("<h2>Invalid username or password.</h2>")

    return render_template("user_login.html", title="Login", form=form)





@app.route("/signup", methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        func = MainFunctions()
        userdata = {}
        userdata['username'] = form.username.data
        userdata['firstname'] = form.firstname.data
        userdata['lastname'] = form.lastname.data
        userdata['email'] = form.email.data
        userdata['password'] = form.password.data
        userdata['zipcode'] = form.zipcode.data
        userdata['isadmin'] = "N"
        func.add_user(userdata)
        flash(f'{form.firstname.data}, your account has been created!', 'success')
        session['admin']='N'
        session['username']=form.username.data
        return redirect(url_for('home', admin=session['admin']))
    return render_template("user_signup.html", title="Sign Up", form=form)



# Display venues for Zip Code
@app.route("/zipsearch", methods=['GET','POST'])
def zipsearch():
    form = ZipSearchForm()
    if form.validate_on_submit():
        func = MainFunctions()
        venuelist = func.get_venues_for_zipcode(form.zipcode.data)
        # return redirect(url_for('venues', list=venuelist))
        return render_template('display_venues.html', list=venuelist)
    return render_template("zip_search.html", title="Search Game", form=form)




# Display venues for Zip Code
@app.route("/datesearch", methods=['GET','POST'])
def datesearch():
    form = DateSearchForm()
    if form.validate_on_submit():
        func = MainFunctions()
        result = func.get_events_for_slot(form.starttime.data, form.endtime.data, form.eventdate.data)
        if(result[0] == 1):
            print(result[1])
            return render_template("venue_events.html", title="Events", list=result[1])
        else:
            return "<h2>"+result[1]+"</h2>"
    return render_template("slotdate_search.html", title="Search Game", form=form)



# Start an Event
@app.route("/startevent", methods=['GET','POST'])
def startevent():
    form = StartEventForm()
    func = CommonFunctions()
    venuelist = func.get_all_venues()
    print("Startevent Body")
    if form.validate_on_submit():

        mainfunc = MainFunctions()
        data = {}
        data['venueid'] = request.form['venue']
        data['username'] = session['username']
        data['eventname'] = form.eventname.data
        data['eventdesc'] = form.eventdesc.data
        data['eventdate'] = form.eventdate.data
        data['starttime'] = form.starttime.data
        data['endtime'] = form.endtime.data
        data['eventcapacity'] = form.eventcapacity.data
        data['genderoption'] = form.genderoption.data

        # result = mainfunc.get_availvenues_for_slot(data['starttime'],data['endtime'],data['eventdate'])
        # available_venue_list = [i[0] for i in result]


        # if data['venueid'] not in available_venue_list:
        #     flash('The venue is not available for given slots on given date. Please try with a different slot or venue.', 'error')
        #     message='The venue is not available for given slots on given date. Please try with a different slot or venue.'
        #     return redirect(url_for('startevent', message=message))

        result = mainfunc.start_event(data)
        if result[0]==0:
            return '<h2>'+result[1]+'</h2>'
        else:
            flash(f'Event: {form.eventname.data} has been started!', 'success')
            return redirect(url_for('home'))
    return render_template("start_event.html", title="Start Event", form=form, list=venuelist, message='')



@app.route("/venueevents", methods=['GET','POST'])
def venueevents():
    func = MainFunctions()
    print(request.form['venue'])
    result = func.display_events_for_venue_id(request.form['venue'])
    print(result[1])
    if(result[0] == 1):
        return render_template("venue_events.html", title="Events", list=result[1])

    else:
        return "<h2>"+result[1]+"</h2>"


@app.route("/editevents", methods=['GET','POST'])
def editevents():
    func = CommonFunctions()
    result = func.get_all_events()
    if(result[0] == 1):
        return render_template("event_list.html", title="Event List", list=result[1], admin=session['admin'])
    else:
        return "<h2>"+result[1]+"</h2>"

@app.route("/removeevent", methods=['GET','POST'])
def removeevent():
    func = MainFunctions()
    # Show joined events of the user
    print(request.form['eventid'])
    result = func.deactivate_event(request.form['eventid'])
    if result[0]==1:
        return redirect(url_for('editevents'))
    else:
        return "<h2>"+result[1]+"</h2"




@app.route("/joinevent", methods=['GET','POST'])
def joinevent():
    func = MainFunctions()
    eventid=request.form['eventid']
    message = func.user_joins_event(session['userid'],eventid)
    return render_template("success_joined.html", title="Event Joined", message=message)



@app.route("/joinedgames", methods=['GET','POST'])
def joinedgames():
    func = MainFunctions()
    result = func.events_joined_user_id(session['userid'])
    # print(result[1])
    if(result[0] == 1):
        return render_template("joined_games.html", title="Joined Games", list=result[1])
    else:
        return "<h2>"+result[1]+"</h2>"

@app.route("/userlist", methods=['GET','POST'])
def userlist():
    func = CommonFunctions()
    list = func.get_all_users()
    return render_template("user_list.html", title="User Directory", list=list, admin=session['admin'])



@app.route("/makeadmin", methods=['GET','POST'])
def makeadmin():
    func = MainFunctions()
    # Show joined events of the user
    result = func.makeadmin_user(request.form['userid'])
    return redirect(url_for('userlist'))

@app.route("/removeuser", methods=['GET','POST'])
def removeuser():
    func = MainFunctions()
    # Show joined events of the user
    print(request.form['userid'])
    result = func.remove_user(request.form['userid'])
    if result[0]==1:
        return redirect(url_for('userlist'))
    else:
        return "<h2>"+result[1]+"</h2"



@app.route("/activateuser", methods=['GET','POST'])
def activateuser():
    func = MainFunctions()
    # Show joined events of the user
    print(request.form['userid'])
    result = func.activate_user(request.form['userid'])
    if result[0]==1:
        return redirect(url_for('userlist'))
    else:
        return "<h2>"+result[1]+"</h2"

@app.route('/now')
def main():
    # When deployed to App Engine, the `GAE_ENV` environment variable will be
    # set to `standard`
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user='root', password='root1234', host=host, db='soccerhoursdb')

    with cnx.cursor() as cursor:
        cursor.execute('SELECT NOW() as now;')
        result = cursor.fetchall()
        current_time = result[0][0]
    cnx.close()

    return str(current_time)
















if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8080,debug=True)

from sqlite3.dbapi2 import Statement
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from flask import url_for
import sqlite3
import datetime, time
import random

app = Flask(__name__)

# sessions configuration
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

SPORTS = [
    "Dodgeball",
    "Soccer",
    "Volleyball",
    "Ultimate frisbee",
    "Football",
    "Netball"
]

# *SQL
# initializing sqlite3 daabase
con = sqlite3.connect("store.db", check_same_thread=False)
db = con.cursor()

def createTables():
    db.execute("CREATE TABLE USERS(USERID TEXT NOT NULL, FIRST_NAME TEXT NOT NULL, LAST_NAME TEXT NOT NULL, DATE_REGISTERED DATETIME NOT NULL, PRIMARY KEY(USERID))")
    db.execute("CREATE TABLE POST( POSTID TEXT NOT NULL, TITLE TEXT NOT NULL, CONTENT TEXT NOT NULL, DATE_CREATED DATETIME NOT NULL, AUTHORID TEXT NOT NULL, PRIMARY KEY(POSTID), FOREIGN KEY (AUTHORID) REFERENCES USERS(USERID))")
    db.execute("CREATE TABLE REGISTRATION(REGID TEXT NOT NULL, FIRST_NAME TEXT NOT NULL, LAST_NAME TEXT NOT NULL, FAVOURITE_SPORT TEXT NOT NULL, TEAM_NAME TEXT NOT NULL, EXPERIENCE TEXT NOT NULL, REG_DATE DATETIME NOT NULL, PLAYERID TEXT NOT NULL, PRIMARY KEY(REGID), FOREIGN KEY(PLAYERID) REFERENCES USERS(USERID))")
    con.commit()
# createTables()

@app.route('/')
def index():
    # username = session.get('firstname')
    if not session.get("firstname"):
        return redirect("/login")
    elif session['firstname']:
        polls = db.execute(
            "SELECT TITLE, CONTENT, DATE_CREATED, AUTHORID FROM POST")
        return render_template("index.html", polls=polls)

@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get("firstname")
        last_name = request.form.get('lastname')
        password=request.form.get("password")
        date_created = datetime.date.today()
        userid = first_name[:3] + last_name[:3]
        # db.execute("ALTER TABLE USERS ADD COLUMN PASSWORD TEXT NULL")
        db.execute("INSERT INTO USERS(USERID, FIRST_NAME, LAST_NAME, DATE_REGISTERED, PASSWORD) VALUES(?,?,?,?,?)",
                (userid.upper(), first_name.capitalize(), last_name.capitalize(), date_created, password))
        con.commit()
        return render_template("success.html")
    if request.method == "GET":
            return render_template('signup.html')

@app.route("/index")
def index1():
    return render_template('index.html')


@app.route("/register", methods=["POST","GET"])
def register():
    if request.method =="POST":
        first_name = request.form.get("firstname")
        last_name = request.form.get("lastname")
        team_name = request.form.get("team")
        favorite_sport = request.form.get("sports")
        reg_date = datetime.date.today()
        exper = request.form.get("experience")
        regid = "REG0" + str(random.randint(0, 5000))
        playerid = first_name[:3] + last_name[:3]
        userid = playerid
    if request.method == "GET":
        return render_template("form.html", sports = SPORTS)

    if not first_name and not last_name and not team_name and not favorite_sport:
        return render_template("error.html", message="you haven't entered any information")
    if not team_name:
        return render_template("error.html", message="missing team name")

    if not favorite_sport:
        return render_template("error.html", message="Missing sport")
    if favorite_sport not in SPORTS:
        return render_template("error.html", message="invalid input")

    db.execute("INSERT INTO REGISTRATION (REGID, FIRST_NAME, LAST_NAME, FAVOURITE_SPORT, TEAM_NAME, EXPERIENCE, REG_DATE, PLAYERID) VALUES(?,?,?,?,?,?,?,?)",
               (regid, first_name, last_name, favorite_sport, team_name, exper, reg_date, playerid.upper()))
    db.execute("INSERT INTO USERS(USERID, FIRST_NAME, LAST_NAME, DATE_REGISTERED) VALUES(?,?,?,?)",
               (userid.upper(), first_name, last_name, reg_date))
    con.commit()

    # *Send emails
    # message = Message("you're registered", recipients=[name])
    # mail.send(message)
    return render_template("success.html")

@app.route("/registrants")
def registrants():
    if session['firstname']:
        registrants = db.execute("SELECT FIRST_NAME, FAVOURITE_SPORT,TEAM_NAME, EXPERIENCE FROM Registration ORDER BY FAVOURITE_SPORT LIMIT 3")
    return render_template("registrants.html", registrants=registrants)

@app.route("/login", methods=["POST", "GET"])
def login():
    time.sleep(0.9)
    if request.method == "POST":
        session["firstname"] = request.form.get("firstname")
        session["lastname"] = request.form.get("lastname")
        print(session["firstname"])
        return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session['firstname'] = None
    return redirect("/")


@app.route("/posts", methods=["POST", "GET"])
def posts():
    if request.method == "GET":
        return render_template("post.html")

    if request.method == "POST":
        _title = request.form.get("title")
        _content = request.form.get("content")
        postid = "POST" + str(int(random.randint(1, 5000)))
        dates = datetime.date.today()
        authorid = session["firstname"]
        
    db.execute("INSERT INTO POST(POSTID, TITLE, CONTENT, DATE_CREATED, AUTHORID) VALUES(?,?,?,?,?)",
               (postid, _title.upper(), _content, dates, authorid.upper()))
    con.commit()

    print(authorid.upper())
    return render_template("index.html")

@app.route("/feed")
def feeds():
    username = session.get("firstname")
    if session["firstname"] == username:
        polls = db.execute(
            "SELECT TITLE, CONTENT, DATE_CREATED, AUTHORID FROM POST WHERE AUTHORID =?", (username,))
        print(username)
    return render_template("feeds.html", polls=polls)

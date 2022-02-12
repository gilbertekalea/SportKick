from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sport.db"
app.config["SECRET_KEY"] = "201020102010"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
from sport import routes

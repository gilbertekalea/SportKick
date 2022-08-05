from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

# from src import app1

#####################################################
#  APPLICATION CONFIGURATIONS AND INSTANCES
# #################################################


# Flask APPLICATION INSTANCE
app = Flask(__name__)

# EMAIL CONFIGURATIONS
mail_settings = {
    "MAIL_SERVER": "smtp.gmail.com",
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ["EMAIL_USERNAME"],
    "MAIL_PASSWORD": os.environ["EMAIL_PASSWORD"],
}

app.config.update(mail_settings)
# Creating an instance for the Mail
mail = Mail(app)


# SQALCHEMY - ORM
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sport.db"
app.config["SECRET_KEY"] = "201020102010"

# DATABASE INSTANCE
db = SQLAlchemy(app)

# CRYPTOGRAPHY INSTANCE
bcrypt = Bcrypt(app)

# LOGIN MANAGEMENT CONFIGURATIONS

login_manager = LoginManager(app)

# REGISTER BLUERINT
from src.view.user import user_bp
from src.view.home import home_bp
from src.view.schedule import sched_bp
from src.view.blog import blog_bp
from src.view.team import team_bp

# BLUEPRINT REGSITRATION
app.register_blueprint(user_bp)
app.register_blueprint(home_bp)
app.register_blueprint(sched_bp)
app.register_blueprint(blog_bp)
app.register_blueprint(team_bp)

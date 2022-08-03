from flask import Blueprint
import datetime, json
from email.generator import DecodedGenerator
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    get_flashed_messages,
    flash,
)
from src.forms import UserLoginForm
from src.forms import UserCreateAccountForm
from .. import db
from src.forms import RegistrationForm, ViewUserProfileForm, CreatePostForm
from src.model.schemas import Attributes, Team, Post, Bookmarks
from src.controller.user import User
from src.utility import schedule
from src.utility.email import ManageEmailTemplate
from src import login_manager, mail
from flask_login import current_user, login_required, login_user, logout_user
from src.utility import blogsview


home_bp = Blueprint('home', __name__, template_folder="templates")
@home_bp.route("/")
def home_page():
    available_teams = Team.query.all()
    return render_template('home_page.html', available_teams=available_teams)
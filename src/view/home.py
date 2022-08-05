from flask import Blueprint, render_template
from src.controller import club

home_bp = Blueprint("home", __name__, template_folder="templates")

@home_bp.route("/")
def home_page():
    available_teams = club.ClubName.convert_to_json()
    return render_template("home_page.html", available_teams=available_teams)

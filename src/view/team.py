from flask import Blueprint, redirect, request, render_template, url_for, flash
from importlib_metadata import method_cache
from .. import db
from flask_login import current_user, login_required, login_user, logout_user
from src.forms import AddSportTeam
from src.controller.club import ClubName, TeamSchema
from src.model import schemas

team_bp = Blueprint("add_team", __name__, template_folder="templates")


@team_bp.route("/team/add-new-team", methods=["POST", "GET"])
def add_team_page():
    schema = TeamSchema()
    team_form = AddSportTeam()
    if request.method == "POST":
        if team_form.validate_on_submit():
            create_new_team = {
                'name':team_form.name.data,
                'description':team_form.description.data,
                'sports':team_form.sports.data,
                'year_formed':team_form.year_formed.data,
                'location':team_form.location.data,
                'stadium':team_form.stadium.data,
            }
            data = schema.load(create_new_team)
            db.session.add(data)
            db.session.commit()
            flash(f"Successfully submitted.", category="success")
            return redirect(url_for("home.home_page"))
        else:
            pass
    if request.method == "GET":
        return render_template("team/add_team.html", team_form=team_form)


# @login_required
# @team_bp.route('/team/delete', methods=['GET'])
# def delete_team():
#     res = ClubName()
#     res.drop_team('Mediators United')

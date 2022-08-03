from src import app
from src.utility import schedule
from flask import Blueprint, render_template
from src.controller import club
from src.model import schemas
# SCHEDULE BLUEPRINT
sched_bp = Blueprint('schedule', '__name__', template_folder='templates')

@sched_bp.route("/schedule/")
def schedule_page():
    payload = schedule.generate_schedule()
    teams = payload[1]
    # This line updates the Team column schedule id;
    # This line is no more relevant since we do not store schedule data on the database.
    # for item in teams:
    #     item = item.strip()
    #     team = ClubName.query.filter_by(name=item + " " + "Soccer Club").first()
        # team.update_schedule_id(team.id)

    fixtures = payload[0]
    main_fixture = []
    # automatically generate fixtures and assign venue and dates to a specific game.
    for i in range(len(fixtures)):
        for j in range(len(fixtures[i])):
            fixture = {}

            # split the two teams playing and use index 1 team to find their stadium name
            # used as a venue for hosting the game

            home_team = fixtures[i][j].split("vs") # extract home team stadiums,
           
        
            t = club.ClubName()
            stad = t.get_club_stadium(home_team[0].strip())
            fixture["fixture"] = fixtures[i][j]
            fixture["venue"] = stad
            # returns time randomly generate.
            fixture["kickoff_time"] = schedule.generate_schedule_date()[0]
            # returns dates -randomly generated
            fixture["kickoff_date"] = schedule.generate_schedule_date()[1]

            main_fixture.append(fixture)

    return render_template("schedule/schedule.html", main_fixture=main_fixture)
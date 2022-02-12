from sport.models import Team
import random
import datetime


def generate_schedule_date():
    # dates
    start_date = datetime.date(2022, 3, 1)
    end_date = datetime.date(2022, 6, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days

    random_number_of_days = random.randrange(days_between_dates)
    random_date = str(start_date + datetime.timedelta(days=random_number_of_days))

    # Hours
    hour = str(random.randint(15, 23))
    minutes = str(random.randint(30, 59))

    kickoff_time = hour + ":" + minutes
    kickoff_date = random_date
    return kickoff_time, kickoff_date


def generate_schedule():

    # for now we create schedule for soccer team;
    team = Team.query.filter_by(sports="Soccer")
    team_name = []
    fixtures = []

    for item in team:
        team_name.append(item.name.replace("Soccer Club", "").strip())
    for name in team_name:
        rand = random.choice(team_name)
        mini_fixture = []
        for rand in team_name:
            if name == rand:
                continue
            else:
                # print(name + ' ' + 'vs' + ' ' + rand)
                table = name + " " + "vs" + " " + rand
                mini_fixture.append(table)
                two_teams = table.split("vs")
        fixtures.append(mini_fixture)
    print("Utility", fixtures)
    return fixtures, two_teams

import datetime
from flask import render_template, request, redirect, url_for, get_flashed_messages, flash, session
from sport.forms import UserLoginForm
from sport.forms import UserCreateAccountForm
from sport import app, db
from sport.forms import RegistrationForm, ViewUserProfileForm, CreatePostForm
from sport.models import User, Attributes, Team, Post, Likes
from sport.utility import utility
from sport import login_manager
from flask_login import current_user, login_required, login_user, logout_user


@app.route('/')
def home_page():
    available_teams = Team.query.all()
    return render_template("home-page.html", available_teams=available_teams)


@app.route('/auth/create-account/', methods=['GET', 'POST'])
def create_account_page():
    signup_form = UserCreateAccountForm()
    if request.method == 'POST':
        if signup_form.validate_on_submit():
            create_user = User(
                username=signup_form.username.data,
                first_name=signup_form.first_name.data,
                last_name=signup_form.last_name.data,
                date_of_birth=signup_form.date_of_birth.data,
                email=signup_form.email.data,
                password=signup_form.password1.data
            )
            db.session.add(create_user)
            db.session.commit()
            flash(
                f'Congratulations!: {signup_form.username.data}, Your Account has been created.',
                category='success')
            return redirect(url_for('login_page', created=True, current_page='login-page'))

        if signup_form.errors != {}:
            for err_msg in signup_form.errors.values():
                flash(f'Oops We got a problem {err_msg}', category='danger')

    return render_template('auth/create-account.html', signup_form=signup_form)


@app.route('/auth/login/', methods=['POST', 'GET'])
def login_page():
    login_form = UserLoginForm()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            attempted_user = User.query.filter_by(
                username=login_form.username.data).first()
            if not attempted_user:
                flash('you dont exit')
            if attempted_user and attempted_user.check_password_correction(user_password=login_form.password.data):
                login_user(attempted_user)
                flash(
                    f'You are logged in as {attempted_user.username}', category='success')
                return redirect(url_for('home_page', user=current_user.username, page='homepage', content_type='available-teams'))
            else:
                flash(
                    f'Sorry! You have entered wrong credentials.', category='danger'
                )
        else:
            flash('SOMETHING WENT WRONG')
    else:
        return render_template('auth/login.html', login_form=login_form)


@app.route('/logout/')
def logout_page():
    logout_user()
    return redirect(url_for('home_page', user='logged-out', content_type='available-teams'))


@app.route("/user/register/", methods=["POST", "GET"])
@login_required
def registration_page():
    register_form = RegistrationForm()

    if request.method == "POST":
        # get's current user
        logged_user = request.form.get('username')
        # Based on players choice on loaded options. return team id of that team;Assign it later to the player.
        registered_team = request.form.get('team_name')
        # if register_form.validate_on_submit():

        player = User.query.filter_by(username=logged_user).first()
        team = Team.query.filter_by(name=registered_team).first()

        # This condition checks whether a current user is registered or not. By checking current' user column is_registered:
        # if it's returns true, it's displays an errror that the user is already registered and can redirect to appropriate pages.

        if player.is_registered:
            attr = Attributes.query.filter_by(id=player.id).first()
            team = Team.query.filter_by(id=player.id).first()
            flash(
                f'Sorry You are alread registered in {attr.sports_registered}, Your team name is: {team.name}', category='info')
        else:
            create_attributes = Attributes(
                skills_level=register_form.experience.data,
                sports_registered=register_form.select_sport.data,
                player_id=player.id
            )
            player.update_user_registration()
            player.update_user_team_id(team)
            flash(f'Thank you We are looking forward to enjoy', category='success')
            # # Then update the user if the user column for=> is_registered, and team_id.
            db.session.add(create_attributes)
            db.session.commit()

            # future improvement => redirects user to the team page where he's registered
            # Can read team decription, view other players and maximum number of players.
        return redirect(url_for('home_page', user=current_user.username, page='home-page', content='available-teams-to-register'))
    if request.method == "GET":
        return render_template("user/registration-form.html", register_form=register_form)


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('This page is restricted to Users with Accounts Only. If you enjoy our services, please follow the recommended instructions Below. ', category='info')
    return render_template('user/registration-form.html')


@app.route('/user/user-profile/', methods=['POST', 'GET'])
@login_required
def view_user_profile():
    if request.method == 'GET':
        blog = Post.query.filter_by(creator_id=current_user.id).all()
        creator = User.query.filter_by(id=blog[0].creator_id).first()
        if current_user.team_id != None:
            team = Team.query.filter_by(id=int(current_user.team_id)).first()
            sport = Attributes.query.filter_by(id=int(current_user.id)).first()
            post = Post.query.filter_by(creator_id=int(current_user.id)).count()
        else:
            team = None
            sport = None
            post= None
        user_profile = ViewUserProfileForm()
        return render_template("user/user-profile.html", user_profile=user_profile, team=team, sport=sport, post=post, blog=blog, creator=creator.first_name)

@app.route('/blog/homepage/', methods=['POST', 'GET'])
@login_required
def blog_page():
    content = CreatePostForm()
    
    # find all posts created by current_user.
    blog = Post.query.filter_by(creator_id=current_user.id).all()
        # creator=User.query.filter_by(id=blog[0].creator_id).first()
   
    if request.method == 'POST':
        create_post = Post(
            post_title=content.post_title.data,
            post_content=content.post_content.data,
            date_created = datetime.datetime.today(),
            creator_id=current_user.id
        )
        db.session.add(create_post)
        db.session.commit()
        flash('Your post has been uploaded !!! ')
        return redirect(url_for('home_page'))
    
    return render_template('blog/blog-create-post.html', content=content, blog=blog)

@app.route('/schedule/')
def schedule_page():
    payload = utility.generate_schedule()
    teams = payload[1]
    # This line updates the Team column schedule id;
    # This line is no more relevant since we do not store schedule data on the database.
    for item in teams:
        item = item.strip()
        team = Team.query.filter_by(name=item + ' ' + 'Soccer Club').first()
        team.update_schedule_id(team.id)

    fixtures = payload[0]
    main_fixture = []
    # automatically generate fixtures and assign venue and dates to a specific game.
    for i in range(len(fixtures)):
        for j in range(len(fixtures[i])):
            fixture = {}

            # split the two teams playing and use index 1 team to find their stadium name
            # used as a venue for hosting the game

            home_team = fixtures[i][j].split(
                'vs')  # extract home team stadiums,
            stad = Team.query.filter_by(
                name=home_team[0] + 'Soccer Club').first()
            fixture['fixture'] = fixtures[i][j]
            fixture['venue'] = stad.stadium
            # returns time randomly generate.
            fixture['kickoff_time'] = utility.generate_schedule_date()[0]
            # returns dates -randomly generated
            fixture['kickoff_date'] = utility.generate_schedule_date()[1]

            main_fixture.append(fixture)

    return render_template('schedule/schedule.html', main_fixture=main_fixture)


@app.route('/create-team/')
def admin_create_team():
    pass

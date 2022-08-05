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
from src import app, db
from src.forms import RegistrationForm, ViewUserProfileForm, CreatePostForm
from src.model.schemas import Attributes, Team, Post, Bookmarks
from src.controller.user import User
from src.utility import schedule
from src.utility.email import ManageEmailTemplate
from src import login_manager, mail
from flask_login import current_user, login_required, login_user, logout_user
from src.utility import blogsview


@app.route("/")
def home_page():
    available_teams = Team.query.all()
    return render_template("home-page.html", available_teams=available_teams)


# @app.route("/auth/create-account/", methods=["GET", "POST"])
# def create_account_page():
#     signup_form = UserCreateAccountForm()
#     if request.method == "POST":
#         if signup_form.validate_on_submit():
#             create_user = User(
#                 username=signup_form.username.data,
#                 first_name=signup_form.first_name.data,
#                 last_name=signup_form.last_name.data,
#                 date_of_birth=signup_form.date_of_birth.data,
#                 email=signup_form.email.data,
#                 password=signup_form.password1.data,
#             )
#             db.session.add(create_user)
#             db.session.commit()

#             person = ManageEmailTemplate(
#                 username=signup_form.username.data,
#                 email=signup_form.email,
#                 first_name=signup_form.first_name,
#                 name='account-creation'
#             )
#             email_template = person.email_channel_composer()
#             mail.send(email_template)

#             flash(
#                 f"Congratulations!: {signup_form.username.data}, Your Account has been created.",
#                 category="success",
#             )
#             return redirect(
#                 url_for("login_page", created=True, current_page="login-page")
#             )

#         if signup_form.errors != {}:
#             for err_msg in signup_form.errors.values():
#                 flash(f"Oops We got a problem {err_msg}", category="danger")

#     return render_template("auth/create-account.html", signup_form=signup_form)


# @app.route("/auth/login/", methods=["POST", "GET"])
# def login_page():
#     login_form = UserLoginForm()
#     if request.method == "POST":
#         if login_form.validate_on_submit():
#             attempted_user = User.query.filter_by(
#                 username=login_form.username.data
#             ).first()
#             if not attempted_user:
#                 flash("you dont exit")
#             if attempted_user and attempted_user.check_password_correction(
#                 user_password=login_form.password.data
#             ):
#                 login_user(attempted_user)
#                 flash(
#                     f"You are logged in as {attempted_user.username}",
#                     category="success",
#                 )
#                 return redirect(
#                     url_for(
#                         "home_page",
#                         user=current_user.username,
#                         page="homepage",
#                         content_type="available-teams",
#                     )
#                 )
#             else:
#                 flash(f"Sorry! You have entered wrong credentials.", category="danger")
#         else:
#             flash("SOMETHING WENT WRONG")
#     else:
#         return render_template("auth/login.html", login_form=login_form)


# @app.route("/logout/")
# def logout_page():
#     logout_user()
#     return redirect(
#         url_for("home_page", user="logged-out", content_type="available-teams")
#     )

# @app.route("/user/register/", methods=["POST", "GET"])
# @login_required
# def registration_page():
#     register_form = RegistrationForm()

#     if request.method == "POST":
#         # get's current user
#         logged_user = request.form.get("username")
#         # Based on players choice on loaded options. return team id of that team;Assign it later to the player.
#         registered_team = request.form.get("team_name")
#         # if register_form.validate_on_submit():

#         player = User.query.filter_by(username=logged_user).first()
#         team = Team.query.filter_by(name=registered_team).first()

#         # This condition checks whether a current user is registered or not. By checking current' user column is_registered:
#         # if it's returns true, it's displays an errror that the user is already registered and can redirect to appropriate pages.

#         if player.is_registered:
#             attr = Attributes.query.filter_by(id=player.id).first()
#             team = Team.query.filter_by(id=player.id).first()
#             flash(
#                 f"Sorry You are alread registered in {attr.sports_registered}, Your team name is: {team.name}",
#                 category="info",
#             )
#         else:
#             create_attributes = Attributes(
#                 skills_level=register_form.experience.data,
#                 sports_registered=register_form.select_sport.data,
#                 player_id=player.id,
#             )
#             player.update_user_registration()
#             player.update_user_team_id(team)

#             flash(f"Successfully submitted.", category="success")

#             # # Then update the user if the user column for=> is_registered, and team_id.
#             db.session.add(create_attributes)
#             db.session.commit()

#             # Send Confirmation Email to User. returns a list object.

#             user = User.query.filter_by(id=current_user.id)
#             for item in user:
#                 meta_data = {
#                     'team':register_form.team_name.data,
#                     'sport_registered': register_form.select_sport.data,
#                     'skills_level':register_form.experience.data
#                 }
#                 # create instance.
#                 template_name = ManageEmailTemplate(username=item.username,email=item.email, first_name=item.first_name, meta_data=meta_data, name='registration')

#                 my_template_message = template_name.email_channel_composer()

#                 # send the email.
#                 mail.send(my_template_message)

#             # future improvement => redirects user to the team page where he's registered
#             # Can read team decription, view other players and maximum number of players.
#         return redirect(
#             url_for(
#                 "home_page",
#                 user=current_user.username,
#                 page="home-page",
#                 content="available-teams-to-register",
#             )
#         )
#     if request.method == "GET":
#         return render_template(
#             "user/registration-form.html", register_form=register_form
#         )


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash(
        "This page is restricted to Users with Accounts Only. If you enjoy our services, please follow the recommended instructions Below. ",
        category="info",
    )
    return render_template("user/registration-form.html")


@app.route("/user/user-profile/personal-data", methods=["POST", "GET"])
@app.route("/user/user-profile/posts-created", methods=["POST", "GET"])
@login_required
def view_user_profile():
    if request.method == "GET":
        blogs = Post.query.filter_by(creator_id=current_user.id).all()
        favourite = Bookmarks.query.filter_by(liker_id=current_user.id).all()

        if current_user.team_id != None:
            team = Team.query.filter_by(id=int(current_user.team_id)).first()
            sport = Attributes.query.filter_by(id=int(current_user.id)).first()
            post = Post.query.filter_by(creator_id=int(current_user.id)).count()
            book = []
            for item in favourite:
                fav_post = Post.query.filter_by(id=item.post_id).first()
                book.append(fav_post)

        else:
            team = None
            sport = None
            post = None
        user_profile = ViewUserProfileForm()
        return render_template(
            "user/user-profile.html",
            user_profile=user_profile,
            team=team,
            sport=sport,
            post=post,
            blogs=blogs,
            fav_post=book,
        )


@app.route("/blog/homepage/", methods=["POST", "GET"])
@login_required
def blog_page():
    content = CreatePostForm()
    # blogs that current_user created.
    user_blogs = (
        Post.query.filter_by(creator_id=current_user.id)
        .order_by(Post.date_created)
        .limit(2)
    )

    # all blogs
    all_blogs = blogsview.blog()

    # all blogs where that current_user has bookmarked.
    bookmarks = Bookmarks.query.all()

    if request.method == "POST":
        # data received when a user clicks on the heart button to signify bookmarks.
        like = request.form.get(
            "post_liked"
        )  # value = 1; used to increase likes count/ bookmarks
        # the current post clicked or bookmarked by user.
        postid = request.form.get("current_post_id")

        if like == "1":
            # ? retrieve all occurances of the current post from the database.
            current_post = Post.query.filter_by(id=int(postid)).first()

            # ? CHECK if current_user and currentpost has been bookedmarked
            # ? Return the bookmarked posts where post_id equals current_post id. The post user clicked.
            book_mark = Bookmarks.query.filter_by(post_id=current_post.id).all()

            #! VALIDATION
            # ? Before taking any actions such as updating the like count;
            # ?We need to verify that the current_post has been bookmarked or liked the current_user.
            for item in book_mark:
                if item.liker_id == current_user.id:
                    flash(
                        "You already liked this post",
                        category="info animate__animated animate__flash",
                    )
                    return redirect(url_for("blog_page"))

            else:
                this_post = Post.query.filter_by(id=int(postid)).first()
                post_bookmark = Bookmarks(
                    post_id=this_post.id, liker_id=current_user.id
                )
                db.session.add(post_bookmark)
                db.session.commit()
                this_post.update_likes(like)
                flash("You have liked this post", category="success")
                return redirect(url_for("blog_page"))

        else:
            create_post = Post(
                post_title=content.post_title.data,
                post_content=content.post_content.data,
                date_created=datetime.datetime.today(),
                creator_id=current_user.id,
            )
            db.session.add(create_post)
            db.session.commit()
            flash("Your post has been uploaded !!! ")
            return redirect(url_for("blog_page"))

    # for get request
    elif request.method == "GET":
        return render_template(
            "blog/blog-create-post.html",
            content=content,
            user_blogs=user_blogs,
            all_blogs=all_blogs,
            bookmarks=bookmarks,
        )
    else:
        flash("Sorry we have no idea what just happen", category="info")


@app.route("/schedule/")
def schedule_page():
    payload = schedule.generate_schedule()
    teams = payload[1]
    # This line updates the Team column schedule id;
    # This line is no more relevant since we do not store schedule data on the database.
    for item in teams:
        item = item.strip()
        team = Team.query.filter_by(name=item + " " + "Soccer Club").first()
        # team.update_schedule_id(team.id)

    fixtures = payload[0]
    main_fixture = []
    # automatically generate fixtures and assign venue and dates to a specific game.
    for i in range(len(fixtures)):
        for j in range(len(fixtures[i])):
            fixture = {}

            # split the two teams playing and use index 1 team to find their stadium name
            # used as a venue for hosting the game

            home_team = fixtures[i][j].split("vs")  # extract home team stadiums,
            stad = Team.query.filter_by(name=home_team[0] + "Soccer Club").first()
            fixture["fixture"] = fixtures[i][j]
            fixture["venue"] = stad.stadium
            # returns time randomly generate.
            fixture["kickoff_time"] = schedule.generate_schedule_date()[0]
            # returns dates -randomly generated
            fixture["kickoff_date"] = schedule.generate_schedule_date()[1]

            main_fixture.append(fixture)

    return render_template("schedule/schedule.html", main_fixture=main_fixture)


@app.route("/create-team/")
def admin_create_team():
    pass

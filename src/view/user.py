from asyncio.log import logger
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
    jsonify,
)
from src.forms import UserLoginForm, ForgotPasswordForm, CheckEmailForm
from src.forms import UserCreateAccountForm
from .. import db
from src.forms import RegistrationForm, ViewUserProfileForm, CreatePostForm
from src.model.schemas import Attributes, Team, Post, Bookmarks
from src.model import schemas
from src.controller.user import User, UserSchema

# from src.utility import schedule
from src.utility.email import ManageEmailTemplate
from src import login_manager, mail
from flask_login import current_user, login_required, login_user, logout_user
# from src.utility import blogsview

# BLUEPRINT
user_bp = Blueprint("user", __name__)


@user_bp.route("/user/create-account", methods=["GET", "POST"])
def create_account_page():
    '''
    Route to handle user account creation
    '''
    schema = UserSchema()
    signup_form = UserCreateAccountForm()
    if request.method == "POST":
        if signup_form.validate_on_submit():
            # create user using schema and then deseralize data 
            create_user = {
                'username':signup_form.username.data,
                'first_name':signup_form.first_name.data,
                'last_name':signup_form.last_name.data,
                'date_of_birth': '2022-08-12',
                'email':signup_form.email.data,
                'password': signup_form.password1.data
            }
            deserialize = schema.load(create_user)
            db.session.add(deserialize)
            db.session.commit()
            # send email confirmation about the user
            person = ManageEmailTemplate(
                username=signup_form.username.data,
                email=signup_form.email,
                first_name=signup_form.first_name,
                name='account-creation'
            )
            # email_template = person.email_channel_composer()
            # mail.send(email_template)

            flash(
                f"Congratulations!: {signup_form.username.data}, Your Account has been created.",
                category="success",
            )
            return redirect(
                url_for("user.login_page", created=True, current_page="login-page")
            )

        if signup_form.errors != {}:
            for err_msg in signup_form.errors:
                flash(f"Oops We got a problem {err_msg}", category="danger")
                return redirect(url_for("user.create_account_page"))

    return render_template("auth/create-account.html", signup_form=signup_form)

@user_bp.route("/auth/login", methods=["POST", "GET"])
def login_page():
    login_form = UserLoginForm()
    if request.method == "POST":
        if login_form.validate_on_submit():
            attempted_user = User.query.filter_by(
                username=login_form.username.data
            ).first()
            # if not attempted_user:
            #     flash("you dont exit")
            if attempted_user and attempted_user.check_password_correction(
                user_password=login_form.password.data
            ):
                login_user(attempted_user)
                flash(
                    f'You are logged in as {attempted_user.username}',
                    category="success",
                )
                return redirect(
                    url_for(
                        "home.home_page",
                        user=current_user.username,
                        page="homepage",
                        content_type="available-teams",
                    )
                )
            else:
                flash(f"Username and password does not match.", category="danger")
                return redirect(url_for("user.login_page"))
        else:
            flash("Something unexpected  happened, please try again")
            return redirect(url_for("user.login_page"))
    else:
        # if request is GET
        # if current_user:
        #     flash('You are login', category='info')
        #     return redirect(url_for('home.home_page'))
        # else:
        return render_template("auth/login.html", login_form=login_form)


@user_bp.route("/logout")
def logout_page():
    logout_user()
    return redirect(
        url_for("home.home_page", user="logged-out", content_type="available-teams")
    )

@user_bp.route("/user/register", methods=["POST", "GET"])
@login_required
def registration_page():
    register_form = RegistrationForm()
    if request.method == "POST":
        # get's current user
        logged_user = request.form.get("username")
        # Based on players choice on loaded options. return team id of that team;Assign it later to the player.
        registered_team = request.form.get("team_name")
        # if register_form.validate_on_submit():

        player = User.query.filter_by(username=logged_user).first()
        team = Team.query.filter_by(name=registered_team).first()

        # This condition checks whether a current user is registered or not. By checking current' user column is_registered:
        # if it's returns true, it's displays an errror that the user is already registered and can redirect to user_bpropriate pages.

        if player.is_registered:
            attr = Attributes.query.filter_by(id=player.id).first()
            team = Team.query.filter_by(id=player.id).first()
            flash(
                f"Sorry You are alread registered in {attr.sports_registered}, Your team name is: {team.name}",
                category="info",
            )
        else:
            create_attributes = Attributes(
                skills_level=register_form.experience.data,
                sports_registered=register_form.select_sport.data,
                player_id=player.id,
            )
            player.update_user_registration()
            player.update_user_team_id(team)

            flash(f"Successfully submitted.", category="success")

            # # Then update the user if the user column for=> is_registered, and team_id.
            db.session.add(create_attributes)
            db.session.commit()

            # Send Registration Confirmation Email to User.
            try:
                user = user.User.query.filter_by(id=current_user.id)
                for item in user:
                    meta_data = {
                        "team": register_form.team_name.data,
                        "sport_registered": register_form.select_sport.data,
                        "skills_level": register_form.experience.data,
                    }
                    # create instance.
                    template_name = ManageEmailTemplate(
                        username=item.username,
                        email=item.email,
                        first_name=item.first_name,
                        meta_data=meta_data,
                        name="registration",
                    )

                    my_template_message = template_name.email_channel_composer()

                    # send the email.
                    mail.send(my_template_message)
            except Exception as e:
                print('Sorry we cant do it')

            # future improvement => redirects user to the team page where he's registered
            # Can read team decription, view other players and maximum number of players.
        return redirect(
            url_for(
                "home.home_page",
                user=current_user.username,
                page="home-page",
                content="available-teams-to-register",
            )
        )
    if request.method == "GET":
        return render_template(
            "user/registration-form.html", register_form=register_form
        )


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash(
        "This page is restricted to Users with Accounts Only. If you enjoy our services, please follow the recommended instructions Below. ",
        category="info",
    )
    return render_template("user/registration-form.html")

@user_bp.route("/user/profile", methods=["POST"])
@login_required
def update_profile():
    user_profile = ViewUserProfileForm()
    # 
    if request.method == 'POST':
        user_id = request.form.get('id')
        cur_user = User.query.filter_by(id=user_id).first()
        updated_data = {
            'id': user_profile.id.data,
            'username': user_profile.username.data,
            'first_name': user_profile.first_name.data,
            'last_name': user_profile.last_name.data,
            'email': user_profile.email.data,
            'date_of_birth': user_profile.date_of_birth.data
        }
        cur_user.update_bio(updated_data)
        return redirect(url_for('home.home_page'))

@user_bp.route("/user/profile", methods=["GET"])
@login_required
def view_user_profile():
    '''
    This view handles operations for users to view their profiles, update information etc.
    '''
    user_profile = ViewUserProfileForm()
    if request.method == "GET":
        my_blogs = Post.query.filter_by(creator_id=current_user.id).all()
        favourite = Bookmarks.query.filter_by(liker_id=current_user.id).all()

        if current_user.team_id != None:
            team = Team.query.filter_by(id=int(current_user.team_id)).first()
            sport = Attributes.query.filter_by(id=int(current_user.id)).first()
            post = Post.query.filter_by(creator_id=int(current_user.id)).count()
            bookmarked_post = []
            for item in favourite:
                fav_post = Post.query.filter_by(id=item.post_id).first()
                bookmarked_post.append(fav_post)
            return render_template(
            "user/user-profile.html",
            user_profile=user_profile,
            team=team,
            sport=sport,
            post=post,
            blogs=my_blogs,
            fav_post = bookmarked_post
        )
        else:
            team = {
                'name': 'N/A'
            }
            sport = {
                'sports_registered':'N/A',
                'skills_level' :'N/A'
                }
            post = 0
    
            return render_template(
            "user/user-profile.html",
            user_profile=user_profile,
            team=team,
            sport=sport,
            post=post,
            blogs=my_blogs,
            # fav_post = bookmarked_post
            )
            
        
# implementing forgot password mechanism.
@user_bp.route("/user/check-email", methods=["GET", "POST"])
def ask_for_email_page():
    """
    This route, checks user by email, if the user is found, we redirect the user to a
    forgot_password_page.

    """
    check_email = CheckEmailForm()
    # First ask user email to verify if they exist in the database.
    if request.method == "GET":
        return render_template("auth/check-email.html", check_email=check_email)

    if request.method == "POST":
        if check_email.validate_on_submit():
            # check if user is in our database by email.
            x_user = User()
            res = x_user.find_user_by_email(check_email.email.data)
            # if user email is found.
            if res:
                # redirect user to forgot_password page.
                return redirect(
                    url_for(
                        "user.forgot_password_page", user_email=check_email.email.data
                    )
                )

            else:
                flash("Sorry we couldnt find that email. Please try again")
                return render_template("auth/check-email.html", check_email=check_email)

@user_bp.route("/user/change-password/<user_email>", methods=["POST", "GET"])
def forgot_password_page(user_email):
    reset_form = ForgotPasswordForm()
    if request.method == "GET":
        return render_template("auth/forgot-password.html", reset_form=reset_form)

    if request.method == "POST":
        x_user = User()
        res = x_user.find_user_by_email(user_email)
        res.reset_password(reset_form.password.data)

        flash(
            "Your password was changed successful, please login to your account",
            category="success",
        )
        return redirect(url_for("user.login_page"))

    
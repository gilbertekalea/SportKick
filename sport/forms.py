from cProfile import label
from email.policy import default
from logging import PlaceHolder
from operator import length_hint
from tkinter.tix import Select
from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, DateField, HiddenField
from wtforms.validators import Length, DataRequired, Email, EqualTo
from sport.models import Team, User, Attributes


# Collects
SPORTS = ['Select', 'Dodgeball', 'Soccer', 'Volleyball',
          'Ultimate Frisbee', 'Football', 'Netball']


EXPERIENCES = ['Select', 'Expert', 'Amateur', 'Professional']


class RegistrationForm(FlaskForm):

    # dynamically display available teams to the users.
    available_teams = Team.query.filter_by(sports='Soccer')
    teams = ['Select',' ']
    for item in available_teams:
        teams.append(item.name)

    first_name = StringField(label='First Name:', validators=[
                             Length(20), DataRequired()])
    last_name = StringField(label='Last Name:', validators=[
        Length(20), DataRequired()])
    team_name = SelectField(label='Team Name:', choices=teams, validators=[
                            Length(min=4), DataRequired()])

    select_sport = SelectField(
        label='Select Sport:', choices=SPORTS, validators=[DataRequired()])

    experience = SelectField(label='Select Experience:',
                             choices=EXPERIENCES, validators=[DataRequired()])

    submit = SubmitField(label='Register')


class UserLoginForm(FlaskForm):
    username = StringField(label='Username', validators=[
                           Length(min=4, max=12), DataRequired()])

    password = PasswordField(label='Password', validators=[
                             Length(min=6), DataRequired()])

    submit = SubmitField(label='Login')


class UserCreateAccountForm(FlaskForm):
    username = StringField(label='Username:', validators=[
                           Length(min=4, max=12), DataRequired()])

    first_name = StringField(label='First Name:', validators=[
                             Length(min=2, max=15), DataRequired()])

    last_name = StringField(label='Last Name:', validators=[
                            Length(min=2, max=15), DataRequired()])

    date_of_birth = DateField(label='Date of Birth',
                              validators=[DataRequired()])
    email = StringField(label='Email', validators=[Email(), DataRequired()])

    password1 = PasswordField(label='Password', validators=[
                              Length(min=6), DataRequired()])

    password2 = PasswordField(label='Confirm Password:', validators=[
                              DataRequired(), EqualTo('password1')])

    submit = SubmitField(label='Create Account:')


class CreatePostForm(FlaskForm):
    post_title = StringField(label='Title:', validators=[
                             Length(min=15, max=50), DataRequired(0)])
    post_content = TextAreaField(label='Description:', validators=[
                                 Length(max=1024), DataRequired()])
    submit = SubmitField(label="Send Post")


class ViewUserProfileForm(FlaskForm):
    id = StringField(label='My Identification', validators=[DataRequired()])
    username = StringField(label='My Username', validators=[DataRequired()])
    first_name = StringField(label='First Name', validators=[DataRequired()])
    last_name = StringField(label='Last Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[Email(), DataRequired()])
    date_of_birth = StringField(label='D.O.B', validators=[DataRequired()])
    team = StringField(label='Registered team', validators=[DataRequired()])
    sport = StringField(label='Sport Registered', validators=[
                        DataRequired()])  # retrieve from attributes
    post = StringField(label='Posts Created', validators=[
                       DataRequired()])  # retrieve from posts
    skill = StringField(label='My Skills', validators=[
                        DataRequired()])  # retrive from attrinutes

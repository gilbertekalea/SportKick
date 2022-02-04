import sched

from sqlalchemy import PrimaryKeyConstraint
from sport import db, bcrypt
from flask_login import UserMixin
from sport import login_manager
import random

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(length=50), nullable=False)
    venue = db.Column(db.String(length=50), nullable=False, default='TBD')
    team_comp = db.Column(db.String(length=1024), nullable=False)
    teams = db.relationship('Team', backref='schedule', lazy=True)


class Team(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=20), nullable=False, unique=True)
    description = db.Column(db.String(length=80), nullable=False)
    sports = db.Column(db.String(length=15), nullable=False)
    max_players = db.Column(db.Integer(), nullable=False, default=10)
    year_formed = db.Column(db.String(length=4), nullable=False)
    location = db.Column(db.String(length=20), nullable=False)
    stadium = db.Column(db.String(length=20), nullable=True)
    # One to Many relationships: A team can register one to many players
    players = db.relationship('User', backref='team', lazy=True)
    # reference schedule id; one entity of a team can have one to many instances of a schedule.
    schedule_id = db.Column(db.Integer, db.ForeignKey(
        'schedule.id'), nullable=False)

    def update_number_of_players(self):
        self.max_players -= 1
        db.session.commit()

    def has_enough_capacity(self):
        return self.max_players > 0

    def update_schedule_id(self, schedule):
        self.schedule_id = schedule
        db.session.commit()
        print('Schedule update!!')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=20), nullable=False, unique=True)
    first_name = db.Column(db.String(length=30), nullable=False, unique=True)
    last_name = db.Column(db.String(length=20), nullable=False, unique=True)
    email = db.Column(db.String(length=20), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=80), nullable=False)
    date_of_birth = db.Column(db.String(length=10), nullable=False)
    team_id = db.Column(db.Integer(), db.ForeignKey('team.id'), nullable=True)
    # updated when user registered for a team or game.
    is_registered = db.Column(db.Boolean(), nullable=True)

    # relationship
    # A user entity can create one to many posts
    posts_created = db.relationship('Post', backref='user', lazy=True)

    # A user entity can have one to many attributes --> skills, type of sports registered.
    # updated when a user register's for a team or game.
    player_attributes = db.relationship(
        'Attributes', backref='user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, password_to_be_hashed):
        self.password_hash = bcrypt.generate_password_hash(
            password_to_be_hashed).decode('utf-8')

    def check_password_correction(self, user_password):
        return bcrypt.check_password_hash(self.password_hash, user_password)

    def update_user_registration(self):
        self.is_registered = True
        db.session.commit()

    def update_user_team_id(self, identity):
        self.team_id = identity.id
        db.session.commit()
        
class Attributes(db.Model):
    '''
    A class of Player attributes. Represent a player skills, sports_registered.
    '''
    id = db.Column(db.Integer(), primary_key=True)
    skills_level = db.Column(db.String(length=20), nullable=False)
    sports_registered = db.Column(db.String(20), nullable=False)
    player_id = db.Column(
        db.Integer(), db.ForeignKey('user.id'), nullable=False)


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    post_title = db.Column(db.String(length=30), nullable=False)
    post_content = db.Column(db.String(length=1024),
                             nullable=False, unique=True)
    date_created = db.Column(db.String(length=14), nullable=False)
    creator_id = db.Column(
        db.Integer(), db.ForeignKey('user.id'), nullable=False)
    
    post_like = db.relationship('Likes', backref='post', lazy=True)

class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    likes = db.Column(db.Integer, nullable=True)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))
    
# team1 = Team(name='Kiwanja Soccer Club', description='We have Passion for Soccer',
#              sports='Soccer', max_players=25, year_formed='1998', location='Montreal', stadium='Tim Hortons Arena', schedule_id=1)
# team2 = Team(name='Mediators Soccer Club', description='We love what we do. The love of Soccer',
#              sports='Soccer', max_players=25, year_formed='2008', location='Toronto', stadium="People Stadium", schedule_id=1)
# team3 = Team(name='Moite Soccer Club', description='Passion for Soccer',
#              sports='Soccer', max_players=25, year_formed='2001', location='Montreal', stadium='Mercier Hochelaga', schedule_id=2)
# team4 = Team(name='Montreal Soccer Club', description='Strive to excell Soccer',
#              sports='Soccer', max_players=25, year_formed='2001', location='Toronto', stadium='Toronto Community Field', schedule_id=2)

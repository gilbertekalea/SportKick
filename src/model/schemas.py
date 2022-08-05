from src import db, bcrypt
from flask_login import UserMixin, current_user
from src import login_manager


class Team(db.Model):
    # when team entity is created
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=20), nullable=False, unique=True)
    description = db.Column(db.String(length=80), nullable=False)
    sports = db.Column(db.String(length=15), nullable=False)
    max_players = db.Column(db.Integer(), nullable=False, default=25)
    year_formed = db.Column(db.String(length=4), nullable=False)
    location = db.Column(db.String(length=20), nullable=False)
    stadium = db.Column(db.String(length=20), nullable=False)
    # One to Many relationships: A team can register one to many players
    players = db.relationship("User", backref="team", lazy=True)
    # reference schedule id; one entity of a team can have one to many instances of a schedule.

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=20), nullable=False, unique=True)
    first_name = db.Column(db.String(length=30), nullable=False)
    last_name = db.Column(db.String(length=20), nullable=False)
    email = db.Column(db.String(length=20), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=80), nullable=False)
    date_of_birth = db.Column(db.String(length=10), nullable=False)
    team_id = db.Column(db.Integer(), db.ForeignKey("team.id"), nullable=True)
    # created only when the user registers for sport.
    # updated when user registered for a team or game.
    is_registered = db.Column(db.Boolean(), nullable=True)

    # updated when user registers.

    # relationship
    user_bookmarked = db.relationship("Bookmarks", backref="user", lazy=True)
    # A user entity can create one to many posts
    posts_created = db.relationship("Post", backref="user", lazy=True)
    # post_liked = db.relationship('Postlikes', backref='user', lazy=True)

    # post_likes => Bolean
    # A user entity can have one to many attributes --> skills, type of sports registered.
    # updated when a user register's for a team or game.
    player_attributes = db.relationship("Attributes", backref="user", lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, password_to_be_hashed):
        self.password_hash = bcrypt.generate_password_hash(
            password_to_be_hashed
        ).decode("utf-8")


class Attributes(db.Model):

    """
    A class of Player attributes. Represent a player skills, sports_registered.
    """

    id = db.Column(db.Integer(), primary_key=True)
    skills_level = db.Column(db.String(length=20), nullable=False)
    sports_registered = db.Column(db.String(20), nullable=False)
    player_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    post_title = db.Column(db.String(length=30), nullable=False)
    post_content = db.Column(db.String(length=1024), nullable=False, unique=True)

    date_created = db.Column(db.String(length=14), nullable=False)
    likes_count = db.Column(db.Integer(), nullable=True, default=0)
    creator_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)

    bookmarked = db.relationship("Bookmarks", backref="post", lazy=True)

    # Basically trying to retrieve the bookmarks post base on relationship.
    # The problems occurs where sometimes it returns false even when the is supposed to be True.
    # Similary with the User methods `user_post_bookmarked`
    # To be revisited.

    # def update_likes(self, like):
    #     if self.likes_count != None:
    #         self.likes_count += int(like)
    #         db.session.commit()
    #     else:
    #         self.likes_count = 0
    #         self.likes_count += int(like)
    #         db.session.commit()


class Bookmarks(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(db.Integer(), db.ForeignKey("post.id"), nullable=True)
    liker_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=True)

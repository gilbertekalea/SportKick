from xml.sax.handler import feature_external_ges
from src.model import schemas
from src import db, bcrypt
from flask_login import UserMixin, current_user
from src import login_manager
from marshmallow import fields, Schema, post_load


class UserSchema(Schema):
    id = fields.String()
    username = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email()
    password = fields.String()
    date_of_birth = fields.String()
    team_id = fields.String()
    is_registered = fields.Boolean()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(schemas.User, UserMixin):

    def get_user_profile(self):
        pass

    def update_bio(self, data):
        '''
        Updates user profile: 
        '''
        self.username = data['username']
        self.date_of_birth = data['date_of_birth']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        db.session.commit()
        
    def reset_password(self, new_password):
        self.password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")
        db.session.commit()

    def check_password_correction(self, user_password):
        return bcrypt.check_password_hash(self.password_hash, user_password)

    def update_user_registration(self):
        self.is_registered = True
        db.session.commit()

    def update_user_team_id(self, identity):
        self.team_id = identity.id
        db.session.commit()

    @classmethod
    def find_user_by_email(cls, email):
        '''
        finds user in the database by email.
        '''
        return cls.query.filter_by(email=email).first()
    
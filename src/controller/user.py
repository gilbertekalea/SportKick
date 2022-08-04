from src.model import schemas
from src import db, bcrypt
from flask_login import UserMixin, current_user
from src import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(schemas.User, UserMixin):
    def reset_password(self, new_password):
        self.password_hash = bcrypt.generate_password_hash(
            new_password
        ).decode("utf-8")
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
        return cls.query.filter_by(email=email).first()
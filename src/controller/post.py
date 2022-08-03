from src import db, bcrypt
from flask_login import UserMixin, current_user
from src import login_manager
from src.model import schemas

class Post(schemas.Post):

    def update_likes(self, like):
        if self.likes_count != None:
            self.likes_count += int(like)
            db.session.commit()
        else:
            self.likes_count = 0
            self.likes_count += int(like)
            db.session.commit()

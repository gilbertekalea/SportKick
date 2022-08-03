from urllib import response
from src.model import schemas
from src import db, bcrypt

class ClubName(schemas.Team):
    
    def drop_team(self, team_name):
        team_obj = self.query.filter_by(name=team_name).first()
        del team_obj
        db.session.commit()

    @classmethod
    def get_club_stadium(cls, name):
       res = cls.query.filter_by(name=name).first()
       return res.stadium

    def update_number_of_players(self):
        self.max_players -= 1
        db.session.commit()

    def has_enough_capacity(self):
        return self.max_players > 0

    def __str__(self) -> str:
        return super().__str__()



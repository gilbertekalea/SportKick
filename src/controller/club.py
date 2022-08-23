from flask import jsonify
from src.model import schemas
from src import db, bcrypt
from marshmallow import fields, Schema, post_load

class TeamSchema(Schema):
    id = fields.String()
    name=fields.String()
    description = fields.String()
    sports = fields.String()
    max_players = fields.String()
    year_formed = fields.String()
    location = fields.String()
    stadium = fields.String()

    @post_load
    def make_team(self, data, **kwargs):
        return Team(**data)

class Team(schemas.Team):
    def drop_team(self, team_name):
        team_obj = self.query.filter_by(name=team_name).first()
        del team_obj
        db.session.commit()
    
    def update_number_of_players(self):
        self.max_players -= 1
        db.session.commit()

    def has_enough_capacity(self):
        return self.max_players > 0

    def __str__(self) -> str:
        return super().__str__()

    @classmethod
    def get_club_stadium(cls, name):
        res = cls.query.filter_by(name=name).first()
        return res.stadium

    @staticmethod
    def convert_to_json():
        teams = Team.query.all()
        jsonify_teams = []
        for obj in teams:
            team = {}
            team['id'] = obj.id
            team['name'] = obj.name
            team['description'] = obj.description
            team['sports']=obj.sports
            team['year_formed'] = obj.year_formed
            team['location'] = obj.location
            team['stadium']= obj.stadium
            team['max_players']=obj.max_players
            jsonify_teams.append(team)
        return jsonify_teams


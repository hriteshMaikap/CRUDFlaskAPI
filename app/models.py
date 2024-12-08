from app import db

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


class Planets(db.Model):
    __tablename__ = 'planets'
    planet_id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String, unique=True, nullable=False)
    planet_type = db.Column(db.String, nullable=False)
    home_star = db.Column(db.String, nullable=False)
    mass = db.Column(db.Float, nullable=False)
    radius = db.Column(db.Float, nullable=False)
    distance = db.Column(db.Float, nullable=False)

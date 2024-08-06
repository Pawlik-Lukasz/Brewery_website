from flask_app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    # breweries = db.relationship('Brewery')

    def __repr__(self):
        return f'<User ("{self.username}", "{self.email}")>'


class Brewery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(60), unique=True)
    country = db.Column(db.String(60), unique=False, nullable=False)
    website = db.Column(db.String(360), unique=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Brewery {self.name}>'

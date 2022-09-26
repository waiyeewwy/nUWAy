from app import db, login, app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))


    def __repr__(self):
        return '<Id: {}, Email: {}>'.format(self.id, self.email)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feedback = db.Column(db.String(255))
    name = db.Column(db.String(128))
    approved = db.Column(db.Boolean)


    def __repr__(self):
        return '<id: {}, feedback: {}, name: {}, approved: {}>'\
            .format(self.id, self.feedback, self.name, self.approved)

    def to_dict(self):
        data = {
            'id': self.id,
            'feedback': self.feedback,
            'name': self.name,
            'approved': self.approved
        }
        return data

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    mimetype = db.Column(db.String(128), nullable=False)
    approved = db.Column(db.Boolean)

    def __repr__(self):
        return '<id: {}, img: {}, name: {}, mimetype: {}, approved: {}>'\
            .format(self.id, self.img, self.name, self.mimetype, self.approved)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    date = db.Column(db.String(128))
    info = db.Column(db.String(255))

    def __repr__(self):
        return '<id: {}, name: {}, date: {}, info: {}}>'\
            .format(self.id, self.name, self.date, self.info)
    
    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'date': self.date,
            'info': self.info
        }
        return data


class Jointeam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    name = db.Column(db.String(128))
    approved = db.Column(db.Boolean)

    def __repr__(self):
        return '<id: {}, name: {}, email: {}}>'\
            .format(self.id, self.name, self.email)
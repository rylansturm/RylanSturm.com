from app import db, login, disney_models
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(100), index=True, unique=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f"<User {self.firstname} {self.lastname}, {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), index=True, unique=True)
    desc = db.Column(db.Text())
    link = db.Column(db.String(100))
    updates = db.relationship("ProjectUpdate", backref="project", lazy="dynamic")

    def __repr__(self):
        return f"<Project {self.name}>"


class ProjectUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    photos = db.relationship("UpdatePhoto", backref="update", lazy="dynamic")
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    title = db.Column(db.String(50))
    text = db.Column(db.Text())

    def __repr__(self):
        return f"<ProjectUpdate '{self.title}' on Project '{self.project.name}'>"

    def __lt__(self, other):
        return self.timestamp < other.timestamp


class UpdatePhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_update_id = db.Column(db.Integer, db.ForeignKey("project_update.id"))
    filename = db.Column(db.String(20))


class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_ip = db.Column(db.String(15))
    page_to = db.Column(db.String(30))
    page_from = db.Column(db.String(30))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f"<Visit to {self.page_to} from {self.page_from} by {self.visitor_ip}>"

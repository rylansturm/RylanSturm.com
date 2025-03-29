from app import db
from datetime import datetime


class AttractionType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True, unique=True)
    attractions = db.relationship(
        "Attraction", backref="attraction_type", lazy="dynamic"
    )

    def __repr__(self):
        return f"<AttractionType {self.name}>"


class Park(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), index=True, unique=True)
    abbreviation = db.Column(db.String(5), index=True, unique=True)
    attractions = db.relationship("Attraction", backref="park", lazy="dynamic")

    def __repr__(self):
        return f"<Park {self.name} ({self.abbreviation})>"


class Attraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    park_id = db.Column(db.Integer, db.ForeignKey("park.id"))
    attractiontype_id = db.Column(db.Integer, db.ForeignKey("attraction_type.id"))
    name = db.Column(db.String(70), index=True, unique=True)
    entries = db.relationship("Entry", backref="attraction", lazy="dynamic")

    def __repr__(self):
        return f"<Project {self.name}>"


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attraction_id = db.Column(db.Integer, db.ForeignKey("attraction.id"))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    comments = db.Column(db.Text)

    def __repr__(self):
        return f"<Entry for {self.attraction}, {self.timestamp}>"

    def __lt__(self, other):
        return self.timestamp < other.timestamp

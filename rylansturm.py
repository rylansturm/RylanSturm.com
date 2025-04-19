import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User
from app.disney_models import (
    AttractionType,
    Attraction,
    Entry,
    Park,
)

@app.shell_context_processor
def make_shell_context():
    return {
        'sa': sa,
        'so': so,
        'db': db,
        'User': User,
        'AttractionType': AttractionType,
        'Attraction': Attraction,
        'Entry': Entry,
        'Park': Park,
    }
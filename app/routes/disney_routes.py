from app import app, db
from app.disney_models import (
    Attraction,
    AttractionType,
    Entry,
    Park,
)
from flask import (
    redirect,
    render_template,
)
from flask_login import (
    current_user,
    login_required,
)


@app.route("/disney")
@login_required
def disney():
    return "DISNEY"

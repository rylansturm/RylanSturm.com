from app import app, db
from app.disney_models import (
    Attraction,
    AttractionType,
    Entry,
    Park,
)
from app.disney_forms import (
    AttractionForm,
    AttractionTypeForm,
    EntryForm,
    ParkForm,
)
from flask import (
    redirect,
    render_template,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
)


@app.route("/disney")
@login_required
def disney():
    return "DISNEY"


@app.route("/disney/parks", methods=["GET", "POST"])
@login_required
def parks():
    form = ParkForm()
    if form.validate_on_submit():
        park = Park(
            name=form.name.data,
            abbreviation=form.abbreviation.data,
        )
        db.session.add(park)
        db.session.commit()
        return redirect(url_for("parks"))
    parks = Park.query.all()
    return render_template("disney/parks.html", form=form, parks=parks)


@app.route("/disney/attraction_types", methods=["GET", "POST"])
@login_required
def attraction_types():
    form = AttractionTypeForm()
    if form.validate_on_submit():
        attraction_type = AttractionType(
            name=form.name.data,
        )
        db.session.add(attraction_type)
        db.session.commit()
        return redirect(url_for("attraction_types"))
    attraction_types = AttractionType.query.all()
    return render_template(
        "disney/attraction_types.html", form=form, attraction_types=attraction_types
    )


@app.route("/disney/attractions", methods=["GET", "POST"])
@login_required
def attractions():
    form = AttractionForm()
    if form.validate_on_submit():
        attraction = Attraction(
            name=form.name.data,
            park_id=form.park_id.data,
            attractiontype_id=form.attractiontype_id.data,
        )
        db.session.add(attraction)
        db.session.commit()
        return redirect(url_for("attractions"))
    form.park_id.choices = [(p.id, p.name) for p in Park.query.order_by("name")]
    form.attractiontype_id.choices = [
        (at.id, at.name) for at in AttractionType.query.order_by("name")
    ]
    attractions = Attraction.query.all()

    return render_template(
        "disney/attractions.html", form=form, attractions=attractions
    )


@app.route("/disney/entries", methods=["GET", "POST"])
@login_required
def entries():
    form = EntryForm()
    if form.validate_on_submit():
        entry = Entry(
            attraction_id=form.attraction_id.data,
            comments=form.comments.data,
        )
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("entries"))
    entries = Entry.query.all()
    return render_template("disney/entries.html", form=form, entries=entries)

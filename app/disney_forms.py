from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateTimeField,
    MultipleFileField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    ValidationError,
)
from app.disney_models import (
    Attraction,
    AttractionType,
    Entry,
    Park,
)


class ParkForm(FlaskForm):
    name = StringField("Park Name", validators=[DataRequired()])
    abbreviation = StringField("Park Abbreviation", validators=[DataRequired()])
    submit = SubmitField("Create Park")

    def validate_name(self, name):
        park = Park.query.filter_by(name=name.data).first()
        if park is not None:
            raise ValidationError("Park name already added.")

    def validate_abbreviation(self, abbreviation):
        park = Park.query.filter_by(abbreviation=abbreviation.data).first()
        if park is not None:
            raise ValidationError("Park abbreviation already added.")


class AttractionTypeForm(FlaskForm):
    name = StringField("Attraction Type", validators=[DataRequired()])
    submit = SubmitField("Create Attraction Type")

    def validate_name(self, name):
        attraction_type = AttractionType.query.filter_by(name=name.data).first()
        if attraction_type is not None:
            raise ValidationError("Attraction type already added.")


class AttractionForm(FlaskForm):
    name = StringField("Attraction Name", validators=[DataRequired()])
    park_id = SelectField("Park", coerce=int)
    attractiontype_id = SelectField("Attraction Type", coerce=int)
    submit = SubmitField("Create Attraction")

    def validate_name(self, name):
        attraction = Attraction.query.filter_by(name=name.data).first()
        if attraction is not None:
            raise ValidationError("Attraction name already added.")

    def validate_park_id(self, park_id):
        park = Park.query.filter_by(id=park_id.data).first()
        if park is None:
            raise ValidationError("Invalid park ID.")

    def validate_attractiontype_id(self, attractiontype_id):
        attraction_type = AttractionType.query.filter_by(
            id=attractiontype_id.data
        ).first()
        if attraction_type is None:
            raise ValidationError("Invalid attraction type ID.")


class EntryForm(FlaskForm):
    attraction_id = StringField("Attraction ID", validators=[DataRequired()])
    timestamp = DateTimeField(
        "Timestamp", format="%Y-%m-%d %H:%M:%S", validators=[DataRequired()]
    )
    comments = TextAreaField("Comments", validators=[DataRequired()])
    submit = SubmitField("Add Entry")

    def validate_attraction_id(self, attraction_id):
        attraction = Attraction.query.filter_by(id=attraction_id.data).first()
        if attraction is None:
            raise ValidationError("Invalid attraction ID.")

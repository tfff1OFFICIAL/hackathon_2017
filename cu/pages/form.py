from wtforms import Form, StringField, validators, TextAreaField, DateTimeField
from cu.database import db_session
from cu.database.models import Organisation


class CreateOrganisationForm(Form):
    name = StringField('Organisation Name', [
        validators.Length(min=4, max=30),
        validators.DataRequired()
        #validators.NoneOf(db_session.query(Organisation.name).all())
                       ]
                       )

    description = TextAreaField(
        'Organisation Description (Markdown supported)'
    )


class CreateEventForm(Form):
    title = StringField(
        'Event title', [
            validators.length(min=4, max=30),
            validators.data_required()
        ]
    )

    datetime = DateTimeField(
        'Event Date and Time (YYYY-mm-dd HH:MM:SS)', [
            validators.DataRequired()
        ]
    )

    location = StringField(
        'Event location', [
            validators.DataRequired()
        ]
    )

    description = TextAreaField(
        'Event Description (Markdown supported)'
    )

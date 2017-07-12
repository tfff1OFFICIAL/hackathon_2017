from wtforms import Form, StringField, validators, TextAreaField
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
        'Organisation Description'
    )

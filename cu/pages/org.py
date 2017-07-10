from flask import Blueprint, session, request
from flask_login import LoginManager
from wtforms import Form, StringField, PasswordField, validators, IntegerField
from cu import app
from cu.database.models import Organisation

org = Blueprint(
    'org',
    __name__,
    template_folder='templates/org'
)

login_mgr = LoginManager()
login_mgr.init_app(app)

class LoginForm(Form):
    username = IntegerField(
        'Organisation ID',
        [
            validators.DataRequired(),
            validators.AnyOf((id for id in Organisation.query(Organisation.id).distinct()))
        ]
    )

    password = PasswordField(
        "Password",
        [validators.DataRequired()]
    )

    

@login_mgr.user_loader
def load_organisation(org_id):
    return Organisation.get(org_id)

@org.route('/')
def main():
    return '<h1>login page if not logged in, or the main page</h1>'

# API
@org.route('/api/login')
def login():
    form =
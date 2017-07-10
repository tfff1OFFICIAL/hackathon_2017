from flask import Blueprint, session, request, abort, redirect, url_for, render_template
from flask_login import LoginManager, login_user
from wtforms import Form, StringField, PasswordField, validators, IntegerField
from cu import login_mgr, app
from cu.util import is_safe_url
from cu.database.models import Organisation

org = Blueprint(
    '/org',
    __name__,
    template_folder='templates'
)


class LoginForm(Form):
    username = IntegerField(
        'Organisation ID',
        [
            validators.DataRequired(),
            validators.AnyOf((id for id in Organisation.query.filter(Organisation.id).distinct()))
        ]
    )

    password = PasswordField(
        "Password",
        [validators.DataRequired()]
    )


@org.record_once
def on_load(state):
    """
    https://stackoverflow.com/questions/20136090/how-do-i-handle-login-in-flask-with-multiple-blueprints
    :param state: state
    :return: None
    """
    org.load_user = load_user
    state.app.login_mgr.b

@login_mgr.user_loader
def load_organisation(org_id):
    return Organisation.get(org_id)


@org.route('/')
def main():
    return '<h1>login page if not logged in, or the main page</h1>'


@org.route('/login')
def login():
    form = LoginForm

    if form.validate():
        login_user(Organisation)

        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)

        return redirect(next or url_for('/'))
    return render_template('org/login.shtml', form=form)

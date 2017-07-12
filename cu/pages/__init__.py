from flask import Blueprint, redirect, url_for
from flask_login import login_required, logout_user, login_user

root = Blueprint(
    '',
    __name__,
    template_folder='templates'
)


@root.route("/")
def index():
    return "<h1>Welcome!</h1>"


@root.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

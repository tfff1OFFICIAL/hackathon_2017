from flask import Blueprint, redirect, url_for
from flask_login import login_required, logout_user, login_user

use = Blueprint(
    '',
    __name__,
    template_folder='templates'
)


@use.route("/")
def index():
    return "<h1>Welcome!</h1>"


@use.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

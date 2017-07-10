from flask import Blueprint, r

use = Blueprint(
    '',
    __name__,
    template_folder='templates'
)


@use.route("/")
def index():
    return "<h1>Welcome!</h1>"

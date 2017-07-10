from flask import Blueprint

org = Blueprint(
    'org',
    __name__,
    template_folder='templates/org'
)


@org.route('/')
def main():
    return '<h1>login page if not logged in, or the main page</h1>'
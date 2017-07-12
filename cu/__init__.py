import os

from flask import Flask, session, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_oauth2_login import GoogleLogin
from flask_misaka import Misaka
from cu import database as db
from cu.database.models import User
from cu import pages
from cu.pages import org, user

app = Flask(
    __name__,
    static_url_path=''
)

app.config.update(
  SECRET_KEY="1245kjehgvikhbewrvn83497wnvwile87hy921u3nf9123nf",
  GOOGLE_LOGIN_REDIRECT_SCHEME="http",
)

for config in (
  "GOOGLE_LOGIN_CLIENT_ID",
  "GOOGLE_LOGIN_CLIENT_SECRET",
):
    app.config[config] = os.environ[config]

app.register_blueprint(pages.root)
app.register_blueprint(org.org, url_prefix="/org")
app.register_blueprint(user.u, url_prefix="/user")

login_manager = LoginManager(app)
googlelogin = GoogleLogin(app)

Misaka(  # Markdown renderer
    app,
    autolink=True,
    fenced_code=True,
    strikethrough=True,
    no_html=True,
    tables=True,
    superscript=True
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login/google')
@app.route('/oauth2callback')
@googlelogin.login_success
def create_or_update_user(token, userinfo, **params):
    user = User.query.filter(User.google_id==userinfo['id']).first()
    if user:
        user.name = userinfo['name']
    else:
        user = User(google_id=userinfo['id'],
                    name=userinfo['name'])
    db.db_session.add(user)
    db.db_session.commit()
    login_user(user)
    return redirect('/')


@app.route('/login')
def login():
    return '<a href="{}">Login with Google</a>'.format(googlelogin.authorization_url())

'''
@app.template_filter('markdown')
def markdown_filter(data):
    """
    Renders MarkDown text as HTML in Jinja templates
    Usage:
    {{ content|markdown }}

    :return: Markup
    """
    from flask import Markup
    from markdown import markdown

    return Markup(markdown(data))
'''

if __name__ == '__main__':
    import pathlib
    if not pathlib.Path("data.db").is_file():
        db.init_db()

    app.run(debug=True)

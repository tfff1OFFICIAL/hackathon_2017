import os

from flask import Flask, session, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_oauth2_login import GoogleLogin
from cu import database as db
from cu.database.models import User
from cu import pages
from cu.pages import org

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

app.register_blueprint(pages.use)
app.register_blueprint(org.org)

login_manager = LoginManager(app)

googlelogin = GoogleLogin(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


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
    print(googlelogin.authorization_url())
    return '<a href="{}">Login with Google</a>'.format(googlelogin.authorization_url())

if __name__ == '__main__':
    import pathlib
    if not pathlib.Path("data.db").is_file():
        db.init_db()

    app.run(debug=True)

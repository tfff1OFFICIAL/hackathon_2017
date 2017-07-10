from flask import Flask, session
from flask_login import LoginManager
from cu import database

app = Flask(
    __name__,
    static_url_path=''
)

app.secret_key = '1245kjehgvikhbewrvn83497wnvwile87hy921u3nf9123nf'

from cu import pages
from cu.pages import org

app.register_blueprint(pages.use)
app.register_blueprint(org.org)

login_mgr = LoginManager()
login_mgr.init_app(app)

if __name__ == '__main__':
    import pathlib
    if not pathlib.Path("data.db").is_file():
        database.init_db()

    app.run(debug=True)

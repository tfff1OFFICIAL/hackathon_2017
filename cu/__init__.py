from flask import Flask, session
from flask_login import LoginManager
from cu import database, pages
from cu.pages import org

app = Flask(
    __name__,
    static_url_path=''
)

app.secret_key = '1245kjehgvikhbewrvn83497wnvwile87hy921u3nf9123nf'

app.register_blueprint(pages.use)
app.register_blueprint(org.org)

if __name__ == '__main__':
    import pathlib
    if not pathlib.Path("data.db").is_file():
        database.init_db()

    app.run(debug=True)

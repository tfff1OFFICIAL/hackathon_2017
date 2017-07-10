from flask import Flask
from cu import database, pages
from cu.pages import org

app = Flask(__name__)

app.register_blueprint(pages.use)
app.register_blueprint(org.org)

if __name__ == '__main__':
    import pathlib
    if not pathlib.Path("data.db").is_file():
        database.init_db()

    app.run(debug=True)

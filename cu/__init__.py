from flask import Flask
from cu import database

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    import pathlib
    if not pathlib.Path("data.db").is_file():
        database.init_db()

    app.run(debug=True)

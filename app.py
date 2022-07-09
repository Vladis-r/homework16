from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from posts_blueprint.routes import routes_Blueprint


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)

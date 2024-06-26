from flask import Flask

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

jwt = JWTManager(app)

from app.model import user, account, node, noderelation
from app import routes

if __name__ == '__main__':
    # Menjalankan aplikasi Flask untuk diakses dari luar
    app.run(host='0.0.0.0')

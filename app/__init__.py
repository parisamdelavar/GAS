from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.users.routes import blueprint as users_blueprint
from app.sponsors.routes import blueprint as sponsors_blueprint
from app.scenarios.routes import blueprint as scenarios_blueprint
import app.exceptions as app_exception
from flask_migrate import Migrate
from . import db_connections


def register_blueprint(app):
    app.register_blueprint(users_blueprint)
    app.register_blueprint(sponsors_blueprint)
    app.register_blueprint(scenarios_blueprint)


def register_error_handlers(app):
    app.register_error_handler(404, app_exception.page_not_found)
    app.register_error_handler(500, app_exception.page_not_found)


app = Flask(__name__)
register_blueprint(app)
register_error_handlers(app)
app.config.from_object('config.DevConfig')
db_connections.init_app(app)


db = SQLAlchemy(app)

from app.users.models import User
from app.sponsors.models import Sponsor
from app.scenarios.models import Scenario
migrate = Migrate(app, db)
# db.create_all()
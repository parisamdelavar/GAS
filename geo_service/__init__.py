from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from geo_service.users.routes import blueprint as users_blueprint
from geo_service.sponsors.routes import blueprint as sponsors_blueprint
from geo_service.scenarios.routes.route_scenario import blueprint as scenarios_blueprint
import geo_service.exceptions as app_exception
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

from geo_service.users.models import User
from geo_service.sponsors.models import Sponsor
from geo_service.scenarios.models.model_scenario import Scenario
migrate = Migrate(app, db)
# db.create_all()
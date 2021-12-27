from flask import Flask
from geo_service.extentions import db

from geo_service.users.routes import blueprint as users_blueprint
from geo_service.sponsors.routes.route_sponsor import blueprint as sponsors_blueprint
from geo_service.scenarios.routes.route_scenario import blueprint as scenarios_blueprint
from geo_service.sponsors.routes.roure_credit_type import blueprint as credit_type_blueprint
import geo_service.exceptions as app_exception
from flask_migrate import Migrate
from . import db_connections


def register_blueprint(app):
    app.register_blueprint(users_blueprint)
    app.register_blueprint(sponsors_blueprint)
    app.register_blueprint(scenarios_blueprint)
    app.register_blueprint(credit_type_blueprint)


def register_error_handlers(app):
    app.register_error_handler(404, app_exception.page_not_found)
    app.register_error_handler(500, app_exception.page_not_found)


app = Flask(__name__)
register_blueprint(app)
register_error_handlers(app)
app.config.from_object('config.DevConfig')
db_connections.init_app(app)


db.init_app(app)

from geo_service.users.models import User
from geo_service.sponsors.models.model_sponsor import Sponsor
from geo_service.scenarios.models.model_scenario import Scenario
migrate = Migrate(app, db)
# db.create_all()

from flask import Blueprint
from flask_restful import Api, Resource, url_for

blueprint = Blueprint('scenario', __name__)
api = Api(blueprint)

@blueprint.route('/a')
def a():
    return 'a'
from flask import Blueprint


blueprint = Blueprint('scenario', __name__)


@blueprint.route('/a')
def a():
    return 'a'
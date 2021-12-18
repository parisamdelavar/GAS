from flask import Blueprint


blueprint = Blueprint('users', __name__)


@blueprint.route('/c')
def c():
    return 'c'

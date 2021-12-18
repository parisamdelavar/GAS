from flask import Blueprint


blueprint = Blueprint('sponsors', __name__)


@blueprint.route('/b')
def b():
    return 'b'

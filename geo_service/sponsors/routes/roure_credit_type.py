from flask import Blueprint, request, jsonify, make_response
from geo_service.decorators import token_required
from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from geo_service.sponsors.models import model_sponsor, model_credit_type
from geo_service.extentions import db
import jwt
import datetime
from flask import current_app as app
from geo_service.decorators import token_required


blueprint = Blueprint('credit_type', __name__)


@blueprint.route('/credittype', methods=['POST'])
@token_required
def create_credit_type(current_user):

    data = request.get_json()
    exist_sponsor = model_sponsor.Sponsor.query.filter_by(name=data["name"]).first()
    if exist_sponsor:
        return jsonify({'message': 'Credit Type is duplicate!'})
    credit_type_default = model_credit_type.CreditType(name=data['name'], description=data['description'])
    db.session.add(credit_type_default)
    db.session.commit()
    return jsonify({'message': 'new credit type created!'})
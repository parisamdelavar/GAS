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
from sqlalchemy import and_, or_, not_


blueprint = Blueprint('sponsors', __name__)


# @blueprint.route('/b')
# def b():
#     return 'b'


@blueprint.route('/sponsor', methods=['POST'])
@token_required
def create_sponsor(current_user):

    data = request.get_json()
    exist_sponsor = model_sponsor.Sponsor.query.filter_by(email=data["email"]).filter_by(status=1).first()
    if exist_sponsor:
        return jsonify({'message': 'Sponsor is duplicate!'})
    credit_type_default = model_credit_type.CreditType.query.filter_by(name='unlimited').first()
    if not credit_type_default:
        credit_type_default = model_credit_type.CreditType(name='unlimited', description='unlimited')
        db.session.add(credit_type_default)
        db.session.flush()
    sponsor = model_sponsor.Sponsor(name=data['name'], email=data['email'], credit_type_id=credit_type_default.id)
    db.session.add(sponsor)
    db.session.flush()
    db.session.commit()
    return jsonify({'message': 'new sponsor created!', 'sponsorId': str(sponsor.public_id)})


@blueprint.route('/sponsor', methods=['GET'])
@token_required
def get_all_sponsor(current_user):

    sponsors = model_sponsor.Sponsor.query.filter_by(status=1).all()
    output = []
    for sponsor in sponsors:
        sponsor_data = {}
        sponsor_data['name'] = sponsor.name
        sponsor_data['email'] = sponsor.email
        sponsor_data['address'] = sponsor.address
        sponsor_data['public_id'] = sponsor.public_id
        output.append(sponsor_data)

    return jsonify({'sponsors': output})

@blueprint.route('/sponsor/<string:id>/', methods=['GET'])
@token_required
def get_sponsor(current_user, id):

    sponsor = model_sponsor.Sponsor.query.filter_by(public_id=id).filter_by(status=1).first()
    if not sponsor:
        return jsonify({'message': 'Sponsor is not Exist'})
    output = []
    sponsor_data = {}
    sponsor_data['name'] = sponsor.name
    sponsor_data['email'] = sponsor.email
    sponsor_data['address'] = sponsor.address
    sponsor_data['public_id'] = sponsor.public_id
    output.append(sponsor_data)

    return jsonify({'sponsor': output})


@blueprint.route('/sponsor/<string:public_id>', methods=['PUT'])
@token_required
def update_sponsor(current_user, public_id):
    data = request.get_json()
    sponsor = model_sponsor.Sponsor.query.filter_by(public_id=public_id).filter_by(status=1).first()
    if not sponsor:
        return jsonify({'message': 'Sponsor is not Exist'})
    if 'email' in data.keys():
        if not model_sponsor.Sponsor.query.filter_by(email=data['email']).first():
            sponsor.email = data['email']
        else:
            return jsonify({'message': 'email is duplicate!'})
    if 'name' in data.keys():
        sponsor.name = data['name']
    if 'address' in data.keys():
        sponsor.name = data['address']
    # if 'credit_type' in data.keys():
    #     c = model_credit_type.CreditType.query.filter_by(name=data['credit_type']).first()
    #     c.sponsors = sponsor

    output = []
    sponsor_data = {}
    sponsor_data['name'] = sponsor.name
    sponsor_data['email'] = sponsor.email
    sponsor_data['address'] = sponsor.address
    sponsor_data['public_id'] = sponsor.public_id
    output.append(sponsor_data )
    db.session.commit()
    return jsonify({'sponsor': output})
    # get_sponsor( public_id)


@blueprint.route('/sponsor/<string:public_id>', methods=['DELETE'])
@token_required
def delete_sponsor(current_user, public_id):
    sponsor = model_sponsor.Sponsor.query.filter_by(public_id=public_id).filter_by(status=1).first()
    if not sponsor:
        return jsonify({'message': 'Sponsor is not Exist'})
    sponsor.status = 0
    db.session.commit()
    return jsonify({'message': 'The Sponsor Was Deleted!'})


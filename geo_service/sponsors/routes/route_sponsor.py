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
    if 'name' not in data.keys():
        return jsonify({'message': 'name is required!'})
    if 'email' not in data.keys():
        return jsonify({'message': 'email is required!'})
    if 'address' not in data.keys():
        return jsonify({'message': 'address is required!'})
    exist_sponsor = model_sponsor.Sponsor.query.filter_by(email=data["email"]).filter_by(status=1).first()
    if exist_sponsor:
        return jsonify({'message': 'Sponsor is duplicate!'})
    credit_type_default = model_credit_type.CreditType.query.filter_by(name='unlimited').first()
    if not credit_type_default:
        credit_type_default = model_credit_type.CreditType(name='unlimited', description='unlimited')
        db.session.add(credit_type_default)
        db.session.flush()
    sponsor = model_sponsor.Sponsor(name=data['name'], email=data['email'], address=data['address'], credit_type_id=credit_type_default.id)
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
        sponsor_data['sponsor_id'] = sponsor.public_id
        sponsor_data['credit tpe'] = sponsor.credit_type.name

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
    sponsor_data['credit tpe'] = sponsor.credit_type.name
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
    sponsor_data['credit tpe'] = sponsor.credit_type.name
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
    return jsonify({'message': 'The Sponsor  Deleted!'})


@blueprint.route('/sponsor/edit_type/<string:public_id>', methods=['POST'])
@token_required
def edit_type_sponsor(current_user, public_id):
    data = request.get_json()
    sponsor = model_sponsor.Sponsor.query.filter_by(public_id=public_id).filter_by(status=1).first()
    if not sponsor:
        return jsonify({'message': 'Sponsor is not Exist'})
    credit_type = model_credit_type.CreditType.query.filter_by(name=data['type']).first()
    sponsor.credit_type_id = credit_type.id
    db.session.commit()
    return jsonify({'message': 'Credit type Was changed!'})

@blueprint.route('/sponsor/credit/<string:public_id>', methods=['GET'])
@token_required
def get_credit_amount_sponsor(current_user, public_id):
    sponsor = model_sponsor.Sponsor.query.filter_by(public_id=public_id).filter_by(status=1).first()
    last_balance_row = model_credit_balance.CreditBalance.query.filter_by(sponsor_id=sponsor.id).order_by(
        model_credit_balance.CreditBalance.log_date.desc()).first()

    output = []
    data = {}
    data['sponsor'] = sponsor.public_id
    data['credit amount'] = last_balance_row.new_balance
    data['credit type'] = sponsor.credit_type.name
    output.append(data)
    return jsonify({'sponsor info': output})


@blueprint.route('/sponsor/add_credit/<string:public_id>/<int:amount>', methods=['POST'])
@token_required
def add_credit__sponsor(current_user, public_id, amount):
    sponsor = model_sponsor.Sponsor.query.filter_by(public_id=public_id).filter_by(status=1).first()
    if not sponsor:
        return jsonify({'message': 'Sponsor is not Exist'})
    if sponsor.credit_type.name == 'unlimited':
        return jsonify({'message': 'This Sponsor is unlimited!'})
    if sponsor.credit_type.name == 'limited':
        last_balance_row = model_credit_balance.CreditBalance.query.filter_by(sponsor_id=sponsor.id).order_by(model_credit_balance.CreditBalance.log_date.desc()).first()
        if last_balance_row:
            new_balance_old = last_balance_row.new_balance
        else:
            new_balance_old = 0

        new_credit_balance = model_credit_balance.CreditBalance(
            sponsor_id=sponsor.id,
            last_balance=new_balance_old,
            credit_amount=amount,
            log_date=datetime.datetime.now(),
            new_balance=int(new_balance_old) + int(amount),
            sponsor_credit_type=sponsor.credit_type.name,
            description="test",
            scenario_id=0,
            schedule_id=0
        )
        db.session.add(new_credit_balance)
        db.session.flush()
        db.session.commit()
    output = []
    data = {}
    data['sponsor'] = sponsor.public_id
    data['credit amount'] = new_credit_balance.new_balance
    data['credit type'] = sponsor.credit_type.name
    output.append(data)
    return jsonify({'sponsor info': output})


@blueprint.route('/sponsor/change_credit_type/<string:public_id>/<string:ctype>', methods=['PUT'])
@token_required
def change_credit_type(current_user, public_id, ctype):
    sponsor = model_sponsor.Sponsor.query.filter_by(public_id=public_id).filter_by(status=1).first()
    if  sponsor is None:
        return jsonify({'message': 'Sponsor is not Exist'})
    current_type = sponsor.credit_type.name
    if current_type == ctype:
        return jsonify({'message': f'Current type is {ctype}!'})
    elif model_credit_type.CreditType.query.filter_by(name=ctype).first() is None:
        return jsonify({'message': f'{ctype} is not defined!'})
    elif model_credit_type.CreditType.query.filter_by(name=ctype).first() is not None:
        id = model_credit_type.CreditType.query.filter_by(name=ctype).first()
        sponsor.credit_type_id = id.id
        db.session.commit()
    output = []
    data = {}
    data['sponsor'] = sponsor.public_id
    data['credit type'] = sponsor.credit_type.name
    output.append(data)
    db.session.commit()
    return jsonify({'sponsor info': output})



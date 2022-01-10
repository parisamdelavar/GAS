from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from geo_service.sponsors.models import model_sponsor, model_credit_type
from geo_service.extentions import db
from geo_service.decorators import token_required
from geo_service.scenarios.models import modell_notification_type, model_scenario_type, model_scenario
from datetime import datetime

blueprint = Blueprint('scenario', __name__)


@blueprint.route('/scenario', methods=['POST'])
@token_required
def create_scenario(current_user):
    # m = modell_notification_type.Notification_Type(name="sms")
    # s = model_scenario_type.Scenario_Type(name="input")
    # db.session.add(m)
    # db.session.add(s)
    # db.session.commit()
    data = request.get_json()
    if 'name' not in data.keys():
        return jsonify({'message': 'name is required!'})
    if 'sponsor_id' not in data.keys():
        return jsonify({'message': 'sponsor_id is required!'})
    if 'notification_type_id' not in data.keys():
        return jsonify({'message': 'notification_type_id is required!'})
    if 'scenario_type_id' not in data.keys():
        return jsonify({'message': 'scenario_type_id is required!'})
    if 'scenario_type_id' not in data.keys():
        return jsonify({'message': 'scenario_type_id is required!'})
    if 'message' not in data.keys():
        return jsonify({'message': 'message is required!'})
    if 'sender_number' not in data.keys():
        return jsonify({'message': 'sender_number is required!'})
    if 'sender_user' not in data.keys():
        return jsonify({'message': 'sender_user is required!'})
    if 'sender_pass' not in data.keys():
        return jsonify({'message': 'sender_pass is required!'})
    if 'delay' not in data.keys():
        return jsonify({'message': 'delay is required!'})

    exist_scenario = model_scenario.Scenario.query.filter_by(name=data["name"]).first()
    if exist_scenario:
        return jsonify({'message': 'Scenario is already exist!'})
    valid_sponsor = model_sponsor.Sponsor.query.filter_by(public_id=data["sponsor_id"]).first()
    if not valid_sponsor:
        return jsonify({'message': 'Sponsor_id is not valid!'})
    valid_notification_type = modell_notification_type.Notification_Type.query.filter_by(
        id=data["notification_type_id"]).first()
    if not valid_notification_type:
        return jsonify({'message': 'NotificationTypeId is not valid!'})
    valid_scenario_type = model_scenario_type.Scenario_Type.query.filter_by(
        id=data["scenario_type_id"]).first()
    if not valid_scenario_type:
        return jsonify({'message': 'ScenarioTypeId is not valid!'})
    scenario_data = model_scenario.Scenario(name=data['name'], priority=1, sponsor_id=valid_sponsor.id,
                                            description=data.get('description'), message=data.get('message'),
                                            scenario_type_id=data['scenario_type_id'], prefix=data.get('prefix'),
                                            create_date=datetime.now(), sender_number=data['sender_number'],
                                            sender_user=data['sender_user'], sender_pass=data['sender_pass'],
                                            status=1, delay=data['delay'], location_limit=1000,
                                            notification_type_id=data['notification_type_id'],
                                            last_modify_date=datetime.now())
    db.session.add(scenario_data)
    db.session.commit()
    return jsonify({'message': 'New scenario created', 'ScenarioId': str(scenario_data.public_id)})


@blueprint.route('/scenario/', methods=['GET'])
@token_required
def get_all_scenario(current_user):
    scenarios = model_scenario.Scenario.query.filter_by(status=1).all()
    if not scenarios:
        return jsonify({'message': 'There is not any active scenario'})
    output = []
    for scenario in scenarios:
        #scenario_data = {}
        scenario_data = {'name': scenario.name, 'description': scenario.description, 'message': scenario.message,
                         'scenario_type_id': scenario.scenario_type_id, 'prefix': scenario.prefix,
                         'sender_number': scenario.sender_number, 'sender_user': scenario.sender_user,
                         'sender_pass': scenario.sender_pass, 'delay': scenario.delay, 'status': scenario.status,
                         'notification_type_id': scenario.notification_type_id, 'public_id': scenario.public_id}
        output.append(scenario_data)
    return jsonify({'scenario': output})


@blueprint.route('/scenario/<string:public_id>', methods=['GET'])
@token_required
def get_scenario(current_user, public_id):
    scenario = model_scenario.Scenario.query.filter_by(public_id=public_id).first()
    if not scenario:
        return jsonify({'message': 'Scenario does not exist'})
    output = []
    scenario_data = {'name': scenario.name, 'description': scenario.description, 'message': scenario.message,
                     'scenario_type_id': scenario.scenario_type_id, 'prefix': scenario.prefix,
                     'sender_number': scenario.sender_number, 'sender_user': scenario.sender_user,
                     'sender_pass': scenario.sender_pass, 'delay': scenario.delay, 'status': scenario.status,
                     'notification_type_id': scenario.notification_type_id, 'public_id': scenario.public_id}
    output.append(scenario_data)
    return jsonify({'scenario': output})


@blueprint.route('/scenario/<string:public_id>', methods=['PUT'])
@token_required
def update_scenario(current_user, public_id):
    data = request.get_json()
    scenario = model_scenario.Scenario.query.filter_by(public_id=public_id).first()
    if not scenario:
        return jsonify({'message': 'Scenario is not exist or is inactive!'})
    if scenario.status == 1:
        return jsonify({'message': 'Active scenario could not being update, please deactivate the scenario first!'})
    if 'name' in data.keys():
        if not model_sponsor.Sponsor.query.filter_by(name=data['name']).filter(public_id != public_id).first():
            scenario.name = data['name']
        else:
            return jsonify({'message': 'The scenario name has been used before!'})
    if 'description' in data.keys():
        scenario.description = data['description']
    if 'message' in data.keys():
        scenario.message = data['message']
    if 'scenario_type_id' in data.keys():
        scenario.scenario_type_id = data['scenario_type_id']
    if 'prefix' in data.keys():
        scenario.prefix = data['prefix']
    if 'sender_number' in data.keys():
        scenario.sender_number = data['sender_number']
    if 'sender_user' in data.keys():
        scenario.sender_user = data['sender_user']
    if 'sender_pass' in data.keys():
        scenario.sender_pass = data['sender_pass']
    if 'delay' in data.keys():
        scenario.delay = data['delay']
    if 'notification_type_id' in data.keys():
        scenario.notification_type_id = data['notification_type_id']
    scenario.last_modify_date = datetime.now()
    output = []
    scenario_data = {'name': scenario.name, 'description': scenario.description, 'message': scenario.message,
                     'scenario_type_id': scenario.scenario_type_id, 'prefix': scenario.prefix,
                     'sender_number': scenario.sender_number, 'sender_user': scenario.sender_user,
                     'sender_pass': scenario.sender_pass, 'delay': scenario.delay,
                     'notification_type_id': scenario.notification_type_id, 'public_id': scenario.public_id}
    output.append(scenario_data)
    db.session.commit()
    return jsonify({'scenario': output})


@blueprint.route('/scenario/activate/<string:public_id>', methods=['PATCH'])
@token_required
def activate_scenario(current_user, public_id):
    scenario = model_scenario.Scenario.query.filter_by(public_id=public_id).first()
    if not scenario:
        return jsonify({'message': 'Scenario does not exist'})
    if scenario.status == 1:
        return jsonify({'message': 'Scenario is already active, noting has been changed'})
    scenario.status = 1
    scenario.last_modify_date = datetime.now()
    # db.session.add(scenario)
    db.session.commit()
    return jsonify({'message': 'Scenario has been activated'})


@blueprint.route('/scenario/deactivate/<string:public_id>', methods=['PATCH'])
@token_required
def deactivate_scenario(current_user, public_id):
    scenario = model_scenario.Scenario.query.filter_by(public_id=public_id).first()
    if not scenario:
        return jsonify({'message': 'Scenario does not exist'})
    if scenario.status == 0:
        return jsonify({'message': 'Scenario is already inactive, noting has been changed'})
    scenario.status = 0
    scenario.last_modify_date = datetime.now()
    # db.session.add(scenario)
    db.session.commit()
    return jsonify({'message': 'Scenario has been deactivate'})


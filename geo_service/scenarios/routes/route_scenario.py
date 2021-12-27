from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource, url_for
from geo_service.sponsors.models import model_sponsor, model_credit_type
from geo_service.extentions import db
from geo_service.decorators import token_required
from geo_service.scenarios.models import modell_notification_type, model_scenario_type, model_scenario
from datetime import datetime

blueprint = Blueprint('scenario', __name__)


# api = Api(blueprint)


@blueprint.route('/a')
def a():
    return 'a'


@blueprint.route('/scenario', methods=['POST'])
@token_required
def create_scenario(current_user):
    data = request.get_json()
    exist_scenario = model_scenario.Scenario.query.filter_by(name=data["name"]).first()
    if exist_scenario:
        return jsonify({'message': 'Scenario is already exist!'})
    valid_sponsor = model_sponsor.Sponsor.query.filter_by(public_id=data["sponsorid"]).first()
    if not valid_sponsor:
        return jsonify({'message': 'SponsorId is not valid!'})
    # notification_type_default = modell_notification_type.Notificatio_Type.query.filter_by(id="1").first()
    valid_notification_type = modell_notification_type.Notificatio_Type.query.filter_by(
        id=data["notification_type_id"]).first()
    if not valid_notification_type:
        return jsonify({'message': 'NotificationTypeId is not valid!'})
    valid_scenario_type = model_scenario_type.Scenario_Type.query.filter_by(
        id=data["scenario_type_id"]).first()
    if not valid_scenario_type:
        return jsonify({'message': 'ScenarioTypeId is not valid!'})
    scenario_data = model_scenario.Scenario(name=data['name'], sponsor_id=data['sponsor_id'],
                                            description=data['description'], message=data['message'],
                                            scenario_type_id=data['scenario_type_id'], prefix=data['prefix'],
                                            create_date=datetime.now(), sender_number=data['sender_number'],
                                            sender_user=data['sender_user'], sender_pass=data['sender_pass'],
                                            status=1, delay=data['delay'], location_limit=1000,
                                            notification_type_id=data['notification_type_id'])
    db.session.add(scenario_data)
    db.session.commit()

    return jsonify({'message': scenario_data.public_id})

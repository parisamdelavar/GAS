from flask import Blueprint, request, jsonify
from geo_service.extentions import db
from geo_service.decorators import token_required
from geo_service.scenarios.models import model_scenario_calender, model_scenario
from datetime import datetime


blueprint = Blueprint('calender', __name__)


@blueprint.route('/calender', methods=['POST'])
@token_required
def create_calender(current_user):
    data = request.get_json()

    exist_scenario = model_scenario.Scenario.query.filter_by(public_id=data["scenario_id"]).first()
    if not exist_scenario:
        return jsonify({'message': 'Scenario is not exist!'})

    calender = model_scenario_calender.Scenario_Calender.query.filter_by(scenario_id=exist_scenario.id).first()
    if calender and calender.status == 1:
        calender.status = 0
        db.session.commit()

    calender_data = model_scenario_calender.Scenario_Calender(scenario_id=exist_scenario.id,
                                                              from_date=datetime.strptime(data["from_date"], '%Y-%m-%d').date(),
                                                              to_date=datetime.strptime(data["to_date"], '%Y-%m-%d').date(),
                                                              status=1, repeat=data["repeat"],
                                                              from_time=datetime.strptime(data["from_time"], '%H:%M:%S').time(),
                                                              to_time=datetime.strptime(data["to_time"], '%H:%M:%S').time(),
                                                              province=data["province"]
                                                              )
    db.session.add(calender_data)
    db.session.commit()
    return jsonify({'message': 'New scenario_calender created'})


@blueprint.route('/calender/<string:public_id>', methods=['GET'])
@token_required
def get_calender(current_user, public_id):
    scenario = model_scenario.Scenario.query.filter_by(public_id=public_id).first()
    if not scenario:
        return jsonify({'message': 'Scenario is not exist'})

    calender = model_scenario_calender.Scenario_Calender.query.filter_by(scenario_id=scenario.id).first()
    if not calender:
        return jsonify({'message': 'Scenario has not calender'})
    output = []
    calender_data = {'scenario_id': calender.scenario_id, 'from_date': str(calender.from_date),
                     'to_date': str(calender.to_date), 'status': calender.status,
                     'repeat': calender.repeat, 'from_time': str(calender.from_time),
                     'to_time': str(calender.to_time), 'province': calender.province}
    output.append(calender_data)
    return jsonify({'calender': output})

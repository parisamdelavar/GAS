from flask import Blueprint, request, jsonify
from geo_service.extentions import db
from geo_service.decorators import token_required
from geo_service.MockAPIs import get_geo_location
from geo_service.scenarios.models import model_scenario_calender, model_scenario, model_location
from datetime import datetime
import requests
import json



blueprint = Blueprint('location', __name__)

@blueprint.route('/location', methods=['POST'])
@token_required
def add_location(current_user):

    data = request.get_json()
    if 'ScenarioID' not in data.keys():
        return jsonify({'message': 'ScenarioID is required!'})
    # if 'Latitude'  in data.keys() or 'longitude' in data.keys():
    #     return jsonify({'message': 'Please send the list of cellIDs in the body.!'})
    if 'Lac_cellIDs' not in data.keys():
        return jsonify({'message': 'cellID list is required!'})
    exist_scenario = model_scenario.Scenario.query.filter_by(public_id=data['ScenarioID']).first()
    if not exist_scenario:
        return jsonify({'message': 'ScenarioID is not  valid!'})
    lac_cellId_list = data['Lac_cellIDs']

    #get info config_db
    for lac, ci in lac_cellId_list:
        # response = requests.get(f"http://10.15.200.86:5003/api/v1/location_info/{lac}/{ci}",verify=False)
        response = get_geo_location(lac, ci)
        PROVINCE = json.loads(response.data)['data']['PROVINCE']
        CITY = json.loads(response.data)['data']['CITY']
        new_locatio = model_location.Location(cell_id=ci, lac_id=lac, status=1, city=CITY, province=PROVINCE, scenario_id=exist_scenario.id, type=model_location.location_type.lac_cell)
        db.session.add(new_locatio)
    db.session.commit()
    return jsonify({'message': 'Locations were added!'})



@blueprint.route('/locationall/<string:scenario>', methods=['DELETE'])
@token_required
def delete_location(current_user, scenario):
    exist_scenario = model_scenario.Scenario.query.filter_by(public_id=scenario).first()
    locations = model_location.Location.query.filter_by(scenario_id=exist_scenario.id).filter_by(status=1).all()
    if not locations:
        return jsonify({'message': 'There is no location for this scenario'})
    for location in locations:
        location.status = 0
    db.session.commit()
    return jsonify({'message': 'Locations Was Deleted!'})


@blueprint.route('/location/<string:scenario>', methods=['GET'])
@token_required
def get_location(current_user, scenario):
    exist_scenario = model_scenario.Scenario.query.filter_by(public_id=scenario).first()
    if not exist_scenario:
        return jsonify({'message': 'ScenarioID is not  valid!'})
    locations = model_location.Location.query.filter_by(scenario_id=exist_scenario.id).filter_by(status=1).all()
    output = []
    for location in locations:
        location_data = {}
        location_data['lac'] = location.lac_id
        location_data['cellId'] = location.cell_id
        location_data['Province'] = location.province
        location_data['city'] = location.city
        output.append(location_data)
    # num_rows_deleted = db.session.query(model_location.Location).delete()
    # db.session.commit()
    return jsonify({'Locations': output})



from flask import current_app, flash, jsonify, make_response, redirect, request


input = {
     'province': 'Tehran',
     'city': 'Tehran',
     'lac_cellId': [['lac1', 'cellid1'], ['lac2', 'cellid2'], ['lac3', 'cellid3']]}


def get_subscribers(input):
    output =[]
    row1 = {
        'subscribernumber': '9100999138',
        'label': 'Moved-Celllevel',
        'EndTime_x': {
            'min': '2021-12-29 11:21:12',
            'max': '2021-12-29 11:21:47'
        },
        'EndTime_y': {
            'max': '2021-12-29 11:21:47'
        },
        'final_label': 'Inbound',
        'lac': '',
        'cellid': ''
    }
    row2 = [{
        'subscribernumber': '9102448145',
        'label': 'FIXED',
        'EndTime_x': {
            'min': '2021-12-29 11:26:44',
            'max': '2021-12-29 11:26:44'
        },
        'EndTime_y': {
            'max': '2021-12-29 11:26:44'
        },
        'final_label': 'Not_Moved',
        'lac': '',
        'cellid': ''
    }]
    output.append(row1)

    output.append(row2)

    return jsonify(output)


def get_geo_location( lac, cell):
    output = {'data': {
              'REGION': 'TEHRAN',
              'PROVINCE': 'TEHRAN',
              'CITY': 'TEHRAN',
              'LAT': '12.545',
              'LNG': '87.65'
    }}
    return jsonify(output)


def latlong_to_laccell(Lat_long_distance):
    output =[]
    output.append(['a', 'b'])
    output.append(['c', 'd'])
    return output


import jwt
import datetime
from flask import current_app as app
from functools import wraps
from flask import Blueprint, request, jsonify, make_response
from geo_service.users.models import User, Role


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is Missing!.'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is Invalid!.'}), 401
        return f(current_user, *args, *kwargs)
    return decorated
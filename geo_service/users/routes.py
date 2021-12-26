from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Role
from geo_service.extentions import db
import jwt
import datetime
from flask import current_app as app
from geo_service.decorators import token_required


blueprint = Blueprint('users', __name__)


@blueprint.route('/user', methods=['GET'])
@token_required
def get_all_user(current_user):
    users = User.query.all()
    output = []
    for user in users:
        user_date = {}
        user_date['public_id'] = user.public_id
        user_date['username'] = user.username
        output.append(user_date)

    return jsonify({'users': output})

@blueprint.route('/user', methods=['POST'])
@token_required
def create_user(current_user):

    data = request.get_json()
    exist_user = User.query.filter_by(username=data["username"]).first()
    if exist_user:
        return jsonify({'message': 'username is duplicate!'})
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    role = Role(role_name="admin", description="admin")
    db.session.add(role)
    db.session.commit()
    new_user.roles.append(role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'new user created!'})



@blueprint.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verufy', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(username = auth.username).first()
    if not user:
        return make_response('Could not verufy', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode()})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})










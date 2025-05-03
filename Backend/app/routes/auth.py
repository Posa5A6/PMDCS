from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.services.auth_service import AuthService
from app.utils.responses import respond

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    result, status = AuthService.create_user(data)
    return respond(result, status)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = AuthService.authenticate_user(data.get('email'), data.get('password'))
    
    if not user:
        return respond({'message': 'Invalid credentials'}, 401)
    
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    return respond({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    })

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return respond({'access_token': new_token})

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = AuthService.get_user(current_user_id)
    return respond({'user': user.to_dict()})
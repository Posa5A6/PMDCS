from app.models import User
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

class AuthService:
    @staticmethod
    def create_user(user_data):
        required_fields = ['username', 'email', 'password', 'role']
        missing = [field for field in required_fields if field not in user_data]
        if missing:
            return {'message': f'Missing fields: {", ".join(missing)}'}, 400

        if User.query.filter((User.email == user_data['email']) | (User.username == user_data['username'])).first():
            return {'message': 'Username or email already exists'}, 400

        try:
            hashed_pw = generate_password_hash(user_data['password'])
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=hashed_pw,
                role=user_data['role'].lower()
            )
            db.session.add(user)
            db.session.commit()
            return user.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

    @staticmethod
    def authenticate_user(email, password):
        user = User.query.filter(func.lower(User.email) == func.lower(email)).first()
        if user and check_password_hash(user.password_hash, password):
            return user
        return None

    @staticmethod
    def get_user(user_id):
        return User.query.get(user_id)
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from app.models.user import User

def roles_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            current_user = User.query.get(get_jwt_identity())
            if current_user.role not in roles:
                return jsonify({"error": "Unauthorized access"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
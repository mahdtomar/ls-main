import jwt
import datetime
from flask import request
from functools import wraps

SECRET_KEY = "your_secret_key"  # Change this to a strong secret key

def generate_jwt(user_id):
    """Generate access token"""
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow(),
        "sub": user_id
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_jwt(token):
    """Decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

def jwt_required(f):
    """Decorator for protecting routes with JWT"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]  # Expecting "Bearer <token>"
        if not token:
            return {"message": "Missing token"}, 401
        
        user_id = decode_jwt(token)
        if not user_id:
            return {"message": "Invalid or expired token"}, 401
        
        return f(user_id, *args, **kwargs)
    return decorated_function

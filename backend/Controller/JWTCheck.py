import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

SECRET_KEY = "your_super_secret_key"
ALGORITHM = "HS256"

def check_jwt_expiry(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"valid": True, "payload": payload}
    except ExpiredSignatureError:
        return {"valid": False, "error": "Token expired"}
    except InvalidTokenError:
        return {"valid": False, "error": "Invalid token"}
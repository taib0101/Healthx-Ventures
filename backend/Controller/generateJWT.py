from datetime import datetime, timedelta, timezone
import jwt

def generateToken(userName):
    expireTime = datetime.now(timezone.utc) + timedelta(minutes=30)

    SECRET_KEY = "secret_key"
    ALGORITHM = "HS256"

    payload = {
        "userName": userName,
        "exp": expireTime
    }

    
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
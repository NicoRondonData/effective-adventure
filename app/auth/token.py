from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import jwt

JWT_ALGORITHM = "HS256"
SECRET = "SECRET"
LIFETIME = 900

def generate_jwt(
    data: dict,
    secret: str = SECRET,
    lifetime_seconds: Optional[int] = LIFETIME,
    algorithm: str = JWT_ALGORITHM,
) -> str:
    payload = data.copy()
    if lifetime_seconds:
        expire = datetime.utcnow() + timedelta(seconds=lifetime_seconds)
        payload["exp"] = expire
    return jwt.encode(payload, secret, algorithm=algorithm)


def decode_jwt(
    encoded_jwt: str,
    secret: str= SECRET,
    algorithms: List[str] = [JWT_ALGORITHM],
) -> Dict[str, Any]:
    return jwt.decode(
        encoded_jwt,
        secret,
        algorithms=algorithms,
    )

def is_valid_token(
    token: str,
    secret: str = SECRET,
    algorithms: List[str] = [JWT_ALGORITHM],
) -> Dict:
    try:
        decoded_token = decode_jwt(token, secret=secret, algorithms=algorithms)
        return {
            "success": "True",
            "status": 200
        }
    except jwt.exceptions.ExpiredSignatureError:
        # El token ha expirado
        return {
            "success": "False",
            "status": 400,
            "error": "Token has expired"
        }
    except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.DecodeError):
        # El token es inválido
        return {
            "success": "False",
            "status": 400,
            "error": "Token is invalid"
        }
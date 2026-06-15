from jose import jwt

SECRET_KEY = "YOURSECRETKEY"
ALGORITHM = "HS256"


def create_access_token(user_id: int):

    payload = {
        "sub": str(user_id)
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_access_token(token: str):

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return payload

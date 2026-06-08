from datetime import datetime, timedelta

from jose import jwt, JWTError

from fastapi import (
    Depends,
    HTTPException,
    Header
)

SECRET_KEY = "neuroflow-secret-key"

ALGORITHM = "HS256"


CLIENTS = {

    "admin": {

        "secret": "admin123",

        "scopes": [
            "query",
            "ingest",
            "admin"
        ]
    },

    "client": {

        "secret": "client123",

        "scopes": [
            "query"
        ]
    }
}


def create_access_token(

    client_id: str,

    scopes: list

):

    expire = datetime.utcnow() + timedelta(
        hours=1
    )

    payload = {

        "sub": client_id,

        "scopes": scopes,

        "exp": expire
    }

    return jwt.encode(

        payload,

        SECRET_KEY,

        algorithm=ALGORITHM
    )


def verify_token(
    token: str
):

    try:

        return jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]
        )

    except JWTError:

        raise HTTPException(

            status_code=401,

            detail="Invalid token"
        )


async def get_current_user(

    authorization: str = Header(None)

):

    if not authorization:

        raise HTTPException(

            status_code=401,

            detail="Missing token"
        )

    if not authorization.startswith(
        "Bearer "
    ):

        raise HTTPException(

            status_code=401,

            detail="Invalid token"
        )

    token = authorization.replace(
        "Bearer ",
        ""
    )

    return verify_token(
        token
    )


def require_scope(scope: str):

    async def checker(

        user=Depends(
            get_current_user
        )

    ):

        if scope not in user.get(
            "scopes",
            []
        ):

            raise HTTPException(

                status_code=403,

                detail="Forbidden"
            )

        return user

    return checker
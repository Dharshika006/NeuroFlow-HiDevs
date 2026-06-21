import os
from datetime import datetime, timedelta
from typing import Sequence
from jose import jwt, JWTError

from fastapi import (
    Depends,
    HTTPException,
    Header
)

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY not configured")

ALGORITHM = "HS256"


CLIENTS = {

    "admin": {

        "secret": os.getenv(
            "ADMIN_CLIENT_SECRET"
        ),

        "scopes": [
            "query",
            "ingest",
            "admin"
        ]
    },

    "client": {

        "secret": os.getenv(
            "CLIENT_CLIENT_SECRET"
        ),

        "scopes": [
            "query"
        ]
    }
}


def create_access_token(

    client_id: str,

    scopes: Sequence[str]

):

    expire = datetime.utcnow() + timedelta(
        hours=1
    )

    payload = {

        "sub": client_id,

        "scopes": list(scopes),

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
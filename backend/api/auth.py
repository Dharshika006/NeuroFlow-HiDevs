from fastapi import APIRouter

from pydantic import BaseModel

from backend.security.auth import (

    CLIENTS,

    create_access_token
)

router = APIRouter()


class TokenRequest(
    BaseModel
):

    client_id: str

    client_secret: str


@router.post("/auth/token")
async def token(
    payload: TokenRequest
):

    client = CLIENTS.get(
        payload.client_id
    )

    if not client:

        return {
            "error":
            "invalid_client"
        }

    if client["secret"] != payload.client_secret:

        return {
            "error":
            "invalid_client"
        }

    token = create_access_token(

        payload.client_id,

        client["scopes"]
    )

    return {

        "access_token":
        token,

        "token_type":
        "bearer",

        "expires_in":
        3600
    }
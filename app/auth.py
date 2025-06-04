from typing import Any

from authlib.integrations.starlette_client import (  # pyright: ignore[reportMissingTypeStubs]
    OAuth,
)
from starlette.datastructures import URL
from starlette.requests import Request

from app.models import AuthTokenResponse


class Auth:
    def __init__(self, client_id: str, client_secret: str, domain: str):
        self.oauth = OAuth()
        self.oauth.register(  # pyright: ignore[reportUnknownMemberType]
            "auth0",
            client_id=client_id,
            client_secret=client_secret,
            client_kwargs={
                "scope": "openid profile email",
            },
            server_metadata_url=f"https://{domain}/.well-known/openid-configuration",
        )

    async def authorise_access_token(self, request: Request) -> AuthTokenResponse:
        token_raw = await self.oauth.auth0.authorize_access_token(  # pyright: ignore
            request
        )
        return AuthTokenResponse(
            **token_raw  # pyright: ignore[reportUnknownArgumentType]
        )

    async def authorise_redirect(self, request: Request, redirect_uri: URL) -> Any:
        return await self.oauth.auth0.authorize_redirect(  # pyright: ignore
            request, redirect_uri=redirect_uri
        )

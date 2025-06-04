from datetime import datetime

from pydantic import BaseModel, EmailStr, HttpUrl


class UserInfo(BaseModel):
    given_name: str
    family_name: str
    nickname: str
    name: str
    picture: HttpUrl
    updated_at: datetime
    email: EmailStr
    email_verified: bool
    iss: str
    aud: str
    sub: str
    iat: int
    exp: int
    sid: str
    nonce: str


class AuthTokenResponse(BaseModel):
    access_token: str
    id_token: str
    scope: str
    expires_in: int
    token_type: str
    expires_at: int
    userinfo: UserInfo

from __future__ import annotations

from datetime import date, datetime
from enum import Enum

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


class FoodGroup(Enum):
    FRUIT = "fruit"
    VEGETABLE = "vegetable"
    WHOLE_GRAIN = "whole_grain"
    LEGUME = "legume"
    NUT = "nut"
    SEED = "seed"
    HERB = "herb"
    SPICE = "spice"
    FUNGI = "fungi"
    TUBER = "tuber"
    SEA_VEGETABLE = "sea_vegetable"
    SPROUT = "sprout"
    FERMENTED = "fermented"
    PSEUDOCEREAL = "pseudocereal"
    FLOWER = "flower"
    OIL = "oil"
    ALGAE = "algae"
    CACTUS = "cactus"
    BAMBOO_SHOOT = "bamboo_shoot"
    PALM_HEART = "palm_heart"


class NewMeal(BaseModel):
    user_id: str
    date: date
    name: str
    food_groups: list[FoodGroup]


class Meal(NewMeal):
    meal_id: int

from __future__ import annotations

from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, HttpUrl
from starlette.datastructures import FormData


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


class Ingredient(BaseModel):
    name: str
    food_group: FoodGroup


class MealType(Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"


class NewMeal(BaseModel):
    user_id: str
    date: date
    name: str
    type: MealType
    ingredients: list[Ingredient]

    @classmethod
    def from_form_data(cls, data: FormData, user_id: str) -> NewMeal:
        maybe_ingredient_names = data.get("ingredient_names[]")
        if not maybe_ingredient_names:
            raise ValueError("Ingredient names are required.")
        maybe_ingredient_groups = data.get("ingredient_groups[]")
        if not maybe_ingredient_groups:
            raise ValueError("Ingredient groups are required.")
        ingredient_names = data.getlist("ingredient_names[]")
        ingredient_groups = data.getlist("ingredient_groups[]")
        if len(ingredient_names) != len(ingredient_groups):
            raise ValueError("Ingredient names and groups must match in length.")

        return NewMeal(
            user_id=user_id,
            name=str(data.get("name")),
            type=MealType(data.get("type")),
            date=(
                datetime.strptime(str(data.get("date")), "%Y-%m-%d").date()
                if data.get("date")
                else date.today()
            ),
            ingredients=(
                [
                    Ingredient(name=str(name), food_group=FoodGroup(fg))
                    for name, fg in zip(ingredient_names, ingredient_groups)
                ]
            ),
        )


class Meal(NewMeal):
    meal_id: int

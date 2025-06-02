from dataclasses import dataclass
from enum import Enum
from typing import Protocol


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


@dataclass(frozen=True)
class Meal:
    meal_id: int
    user_id: str
    name: str
    good_groups: list[FoodGroup]


class MealRepoProtocol(Protocol):
    async def get(self, meal_id: int) -> Meal: ...

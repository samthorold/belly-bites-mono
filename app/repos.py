from typing import Protocol

from app.models import Meal


class MealRepoProtocol(Protocol):
    async def get(self, meal_id: int) -> Meal: ...

    async def create(self, meal: Meal) -> Meal: ...

    async def get_for_user(self, user_id: str) -> list[Meal]: ...

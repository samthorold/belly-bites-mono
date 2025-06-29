from typing import Protocol

from app.models import Meal, NewMeal


class MealRepoProtocol(Protocol):
    async def get(self, meal_id: int) -> Meal: ...

    async def create(self, meal: Meal) -> Meal: ...

    async def get_for_user(self, user_id: str) -> list[Meal]: ...


class InMemoryMealRepo:
    def __init__(self):
        self.meals: list[Meal] = []

    async def get(self, meal_id: int) -> Meal:
        for meal in self.meals:
            if meal.meal_id == meal_id:
                return meal
        raise ValueError(f"Meal with id {meal_id} not found")

    async def create(self, new_meal: NewMeal) -> Meal:
        meal_id = len(self.meals) + 1
        meal = Meal(
            meal_id=meal_id,
            user_id=new_meal.user_id,
            date=new_meal.date,
            name=new_meal.name,
            type=new_meal.type,
            food_groups=new_meal.food_groups,
        )
        self.meals.append(meal)
        return meal

    async def get_for_user(self, user_id: str) -> list[Meal]:
        return [meal for meal in self.meals if meal.user_id == user_id]

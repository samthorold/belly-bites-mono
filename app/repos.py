from typing import Protocol

from app.models import Meal, NewMeal


class MealRepoProtocol(Protocol):
    async def get(self, meal_id: int) -> Meal: ...

    async def create(self, meal: Meal) -> Meal: ...

    async def get_for_user(self, user_id: str) -> list[Meal]: ...

    async def delete(self, meal_id: int) -> None: ...


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
            ingredients=new_meal.ingredients,
        )
        self.meals.append(meal)
        return meal

    async def get_for_user(self, user_id: str) -> list[Meal]:
        return [meal for meal in self.meals if meal.user_id == user_id]

    async def update(self, meal_id: int, new_meal: NewMeal) -> Meal:
        for i, meal in enumerate(self.meals):
            if meal.meal_id == meal_id:
                updated_meal = Meal(
                    meal_id=meal_id,
                    user_id=new_meal.user_id,
                    date=new_meal.date,
                    name=new_meal.name,
                    type=new_meal.type,
                    ingredients=new_meal.ingredients,
                )
                self.meals[i] = updated_meal
                return updated_meal
        raise ValueError(f"Meal with id {meal_id} not found")

    async def delete(self, meal_id: int) -> None:
        self.meals = [meal for meal in self.meals if meal.meal_id != meal_id]

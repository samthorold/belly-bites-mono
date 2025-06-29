import logging
from typing import Any

from jinja2 import Environment, PackageLoader, select_autoescape
from starlette.applications import Starlette
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.routing import Route

from app.auth import Auth
from app.config import Settings
from app.models import FoodGroup, MealType, NewMeal, UserInfo
from app.repos import InMemoryMealRepo

settings = Settings()

logging.basicConfig(
    level=settings.LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


logger.info(settings)


templates = Environment(loader=PackageLoader("app"), autoescape=select_autoescape())


auth = Auth(
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET.get_secret_value(),
    domain=settings.AUTH0_DOMAIN,
)

meals_repo = InMemoryMealRepo()


async def home(request: Request) -> HTMLResponse | RedirectResponse:
    user = request.session.get("user")
    user_name = UserInfo.model_validate_json(user).given_name if user else "Anon"
    template = templates.get_template("home.html")
    return HTMLResponse(template.render(app_name=settings.APP_NAME, user=user_name))


async def meals(request: Request) -> HTMLResponse | RedirectResponse:
    user = request.session.get("user")
    if user is None:
        logger.info("User not logged in, redirecting to login")
        return RedirectResponse(url="/login")
    user_info = UserInfo.model_validate_json(user)

    if request.method == "POST":
        data = await request.form()
        logger.info("%s create meal %s", user_info.sub, data)
        new_meal = NewMeal.from_form_data(data, user_info.sub)
        meal = await meals_repo.create(new_meal)
        logger.info("%s meal created: %s", user_info.sub, meal)
        return RedirectResponse(url=request.url_for("meals"), status_code=303)

    user_meals = await meals_repo.get_for_user(user_info.sub)
    template = templates.get_template("meals.html")
    return HTMLResponse(
        template.render(user=user_info, meals=user_meals, request=request)
    )


async def create_meal(request: Request) -> HTMLResponse | RedirectResponse:
    user = request.session.get("user")
    if user is None:
        logger.info("User not logged in, redirecting to login")
        return RedirectResponse(url="/login")
    user_info = UserInfo.model_validate_json(user)

    template = templates.get_template("create_meal.html")
    return HTMLResponse(
        template.render(
            food_groups=list(FoodGroup),
            meal_types=list(MealType),
            request=request,
            user=user_info,
        )
    )


async def callback(request: Request) -> RedirectResponse:
    token = await auth.authorise_access_token(request)
    request.session["user"] = token.userinfo.model_dump_json()
    return RedirectResponse(url="/")


async def login(request: Request) -> Any:
    redirect_uri = request.url_for("callback")
    logger.info("Redirect URI: %s", redirect_uri)
    return await auth.authorise_redirect(request, redirect_uri=redirect_uri)


async def logout(request: Request) -> RedirectResponse:
    request.session.pop("user", None)
    url = auth.logout_url(return_to=str(request.url_for("home")))
    logger.info("Logout URL: %s", url)
    return RedirectResponse(url=url)


app = Starlette(
    routes=[
        Route("/", home, methods=["GET"], name="home"),
        Route("/login", login, methods=["GET"], name="login"),
        Route("/logout", logout, methods=["GET"], name="logout"),
        Route("/callback", callback, methods=["GET", "POST"], name="callback"),
        Route("/meals", meals, methods=["GET", "POST"], name="meals"),
        Route("/meals/create", create_meal, methods=["GET"], name="create_meal"),
    ]
)

app.add_middleware(
    SessionMiddleware, secret_key=settings.APP_SECRET_KEY.get_secret_value()
)

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
from app.models import UserInfo

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


async def home(request: Request) -> HTMLResponse | RedirectResponse:
    user = request.session.get("user")
    logger.info("User session: %s", user)
    # if user is None:
    #     logger.info("User not logged in, redirecting to login")
    #     return RedirectResponse(url="/login")
    user = UserInfo.model_validate_json(user).given_name if user else "Anon"
    template = templates.get_template("home.html")
    return HTMLResponse(template.render(app_name=settings.APP_NAME, user=user))


async def callback(request: Request) -> RedirectResponse:
    token = await auth.authorise_access_token(request)
    logger.info("Token received: %s", token)
    request.session["user"] = token.userinfo.model_dump_json()
    return RedirectResponse(url="/")


async def login(request: Request) -> Any:
    redirect_uri = request.url_for("callback")
    logger.info("Redirect URI: %s", redirect_uri)
    return await auth.authorise_redirect(request, redirect_uri=redirect_uri)


async def logout(request: Request) -> RedirectResponse:
    request.session.pop("user", None)
    url = "https://" + settings.AUTH0_DOMAIN + "/v2/logout"
    url += "?returnTo=" + str(request.url_for("home"))
    url += "&client_id=" + settings.AUTH0_CLIENT_ID
    logger.info("Logout URL: %s", url)
    return RedirectResponse(url=url)


app = Starlette(
    routes=[
        Route("/", home, methods=["GET"], name="home"),
        Route("/login", login, methods=["GET"], name="login"),
        Route("/logout", logout, methods=["GET"], name="logout"),
        Route("/callback", callback, methods=["GET", "POST"], name="callback"),
    ]
)

app.add_middleware(
    SessionMiddleware, secret_key=settings.APP_SECRET_KEY.get_secret_value()
)

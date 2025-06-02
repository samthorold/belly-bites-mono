import logging
from typing import Any

from authlib.integrations.starlette_client import (  # pyright: ignore[reportMissingTypeStubs]
    OAuth,
)
from jinja2 import Environment, PackageLoader, select_autoescape
from starlette.applications import Starlette
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.routing import Route

from app.config import Settings

settings = Settings()

logging.basicConfig(
    level=settings.LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


logger.info(settings)


templates = Environment(loader=PackageLoader("app"), autoescape=select_autoescape())


oauth = OAuth()
oauth.register(  # pyright: ignore[reportUnknownMemberType]
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


async def home(request: Request) -> HTMLResponse:
    user = request.session.get("user")
    logger.info("User session: %s", user)
    template = templates.get_template("home.html")
    return HTMLResponse(template.render(app_name=settings.APP_NAME))


async def callback(request: Request) -> RedirectResponse:
    auth0 = oauth.create_client("auth0")
    token = await auth0.authorize_access_token(request)
    user = token["userinfo"]
    logger.info("User info: %s", user)
    if user:
        request.session["user"] = user
    return RedirectResponse(url="/")


async def login(request: Request) -> Any:
    auth0 = oauth.create_client("auth0")
    redirect_uri = request.url_for("callback")
    logger.info("Redirect URI: %s", redirect_uri)
    return await auth0.authorize_redirect(request, redirect_uri)


app = Starlette(
    routes=[
        Route("/", home, methods=["GET"], name="home"),
        Route("/login", login, methods=["GET"], name="login"),
        Route("/callback", callback, methods=["GET", "POST"], name="callback"),
    ]
)

app.add_middleware(SessionMiddleware, secret_key=settings.APP_SECRET_KEY)

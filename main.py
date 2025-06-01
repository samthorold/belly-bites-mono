import logging

from jinja2 import Environment, PackageLoader, select_autoescape
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Route

from app.config import Settings

settings = Settings()

logging.basicConfig(
    level=settings.LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


logger.info(settings)


templates = Environment(loader=PackageLoader("app"), autoescape=select_autoescape())


async def home(request: Request) -> HTMLResponse:
    template = templates.get_template("home.html")
    return HTMLResponse(template.render(app_name=settings.APP_NAME))


app = Starlette(
    routes=[
        Route("/", home, methods=["GET"]),
    ]
)

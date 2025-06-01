from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Route


async def home(request: Request) -> HTMLResponse:
    return HTMLResponse("<h3>Belly Bites</h3><p>Welcome to Belly Bites!</p>")


app = Starlette(
    routes=[
        Route("/", home, methods=["GET"]),
    ]
)

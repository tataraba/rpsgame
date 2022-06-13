from fastapi import FastAPI

from app.mylib.util import incl_static
from app.routes import router


def get_app() -> FastAPI:

    app = FastAPI(title="Rock Paper Scissors", version="0.0.1")

    incl_static(app)  # Mount static files in /static directory
    app.include_router(router)  # Register routes in `routes` module
    return app


app = get_app()

from pathlib import Path

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

project_root = Path(__file__).parent.parent


def init_template() -> Jinja2Templates:
    print(project_root / "templates")
    return Jinja2Templates(project_root / "templates")


def incl_static(app: FastAPI) -> None:
    app.mount("/static", StaticFiles(directory=project_root / "static"), name="static")

from fastapi.routing import APIRouter

from .game import router

web_router = APIRouter()

web_router.include_router(router, tags=["main"])

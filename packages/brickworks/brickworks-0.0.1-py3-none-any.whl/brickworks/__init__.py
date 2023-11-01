from fastapi import FastAPI

from brickworks.bricks import get_bricks
from brickworks.db import DBSessionMiddleware
from brickworks.settings import BrickworksSettings
from brickworks.utils.loader import import_object_from_path


def create_app(settings: BrickworksSettings | None = None, for_testing=False) -> FastAPI:
    settings = settings or BrickworksSettings()

    app_base = FastAPI()
    app_api = FastAPI()

    if not for_testing:
        # if we run the app with testclient we will create sessions ourselves, so we can roll back
        app_api.add_middleware(DBSessionMiddleware, settings=settings)

    for brick in get_bricks(settings):
        _add_routers(app_api, brick.routers)

    app_base.mount("/api", app_api)
    return app_base


def _add_routers(app: FastAPI, routers: list[str]) -> None:
    for router_path in routers:
        router = import_object_from_path(router_path)
        app.include_router(router)

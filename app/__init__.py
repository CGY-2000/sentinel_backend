from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.init_app import make_middlewares, register_exceptions, register_routers
from app.databse import db_init, de_deinit
from app.databse.curds.users import user_init


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_init()
    await user_init()
    yield
    await de_deinit()


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        middleware=make_middlewares()
    )
    register_exceptions(app)
    register_routers(app)
    return app
from apis.base import api_router
from util.config import settings
from db.base import Base
from db.session import engine
from db.utils import check_db_connected
from db.utils import check_db_disconnected
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from web.base import api_router as web_app_router
from fastapi.middleware.cors import CORSMiddleware


def create_logger():
    from logging.config import dictConfig
    import logging
    from util.log import LogConfig

    dictConfig(LogConfig().dict())
    logger = logging.getLogger(settings.LOGGER_NAME)
    logger.info("Logger initialized")


def include_router(app):
    app.include_router(api_router)
    app.include_router(web_app_router)


def configure_static(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT, version=settings.VERSION)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    create_logger()
    include_router(app)
    configure_static(app)
    create_tables()
    return app


app = start_application()


@app.on_event("startup")
async def app_startup():
    await check_db_connected()


@app.on_event("shutdown")
async def app_shutdown():
    await check_db_disconnected()

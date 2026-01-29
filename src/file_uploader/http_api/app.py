import asyncio
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import APIRouter, FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from file_uploader.http_api.controllers import upload_files_router
from file_uploader.http_api.settings import HttpApiSettings

root_router = APIRouter()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """
    Выполняет действия перед запуском и после завершения основного приложения
    """
    logger = logging.getLogger("FastAPI lifespan")
    logger.info("Загрузка lifespan...")

    api_settings: HttpApiSettings = app.state.api_settings

    await _create_files_dir(api_settings=api_settings)

    logger.info("Lifespan загружен")
    yield
    logger.info("Выполняется очистка lifespan...")

    logger.info("Очистка lifespan завершена")


async def _create_files_dir(api_settings: HttpApiSettings) -> None:
    files_dir = Path(api_settings.FILES_DIR)
    await asyncio.to_thread(files_dir.mkdir, parents=True, exist_ok=True)


def create_app(api_settings: HttpApiSettings) -> FastAPI:
    """
    Создаёт инстанс fast api
    """
    app = FastAPI(
        title="File uploader",
        lifespan=lifespan,
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=api_settings.get_formated_cors_allow_origins(),
                allow_credentials=api_settings.CORS_ALLOW_CREDENTIALS,
                allow_methods=api_settings.get_formated_cors_allow_methods(),
                allow_headers=api_settings.get_formated_cors_allow_headers(),
            )
        ],
        debug=api_settings.HTTP_API_DEBUG_MODE,
    )

    app.include_router(root_router)
    api_router = APIRouter(prefix="/api")

    api_router.include_router(upload_files_router)

    app.include_router(api_router)

    app.state.api_settings = api_settings

    return app


@root_router.get("/", include_in_schema=False)
async def docs_redirect() -> RedirectResponse:
    """
    Редирект на страницу документации
    """
    return RedirectResponse(url="/docs")

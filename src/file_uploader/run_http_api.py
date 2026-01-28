import logging

import uvicorn

from file_uploader import log
from file_uploader.http_api.app import create_app
from file_uploader.http_api.settings import HttpApiSettings

api_settings = HttpApiSettings()


log_config = log.create_config(
    api_settings.LOGGING_CONFIG,
)
log.configure(
    api_settings.LOGGING_CONFIG,
)


app = create_app(
    api_settings=api_settings,
)

if __name__ == "__main__":
    logger = logging.getLogger("UvicornDevServer")
    logger.warning("HTTP API запущено в режиме разработки")

    uvicorn.run(
        "file_uploader.run_http_api:app",
        host="localhost",
        log_level="debug",
        log_config=log_config,
    )

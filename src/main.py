import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.config.config import APP_CONFIG
from src.db.check import db_settings_initializations
from src.db.engine import get_db_engine
from src.exceptions.app import AppException
from src.helper.logging import init_loggers
from src.models.http_response_code import HTTPResponseCode
from src.router.author import router as author_router
from src.router.book import router as book_router
from src.router.docs import router as docs_router
from src.router.health import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # noqa: PLR0915
    """Application startup and shutdown context manager."""
    init_loggers(APP_CONFIG)
    logger = logging.getLogger("app")
    try:
        db_settings_initializations()
        logger.info("Starting up the application...")
        yield
    except Exception as exc:
        logger.error(f"An error occurred during application startup: {str(exc)}")
        raise exc
    finally:
        #  Close all open db pool connections
        logger.info("Shutting down the application...")
        engine = get_db_engine()
        engine.dispose()
        logger.info("All DB pool connections are closed")


description = """
The system for managing its book stock. In order to properly manage this library,
system users must be able to :

- Add, modify and delete authors
- Add, modify and delete books
- Manage book loans and stock"""

app = FastAPI(
    title="Create a simple application to manage municipal library system.",
    description=description,
    lifespan=lifespan,
)


@app.exception_handler(Exception)
async def exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    """Application level exception handler."""
    if isinstance(exc, AppException):
        ex = exc
    else:
        ex = AppException(
            message=str(exc),
            status_code=HTTPResponseCode.INTERNAL_SERVER_ERROR,
        )

    ex.log_exception()
    return ex.to_json_response()


# Manually add all routers to the FastApi application
app.include_router(docs_router)
app.include_router(health_router)
app.include_router(author_router)
app.include_router(book_router)

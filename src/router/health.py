from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.models.http_response_code import HTTPResponseCode

router = APIRouter()


@router.get("/health", include_in_schema=False)
def health_check() -> JSONResponse:
    return JSONResponse(status_code=HTTPResponseCode.OK, content={"status": "ok"})

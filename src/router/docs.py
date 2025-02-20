from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/", include_in_schema=False)
def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="/docs")

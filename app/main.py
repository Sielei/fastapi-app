from fastapi import FastAPI
from fastapi.security import HTTPBearer
from starlette.responses import RedirectResponse

from app.api.main import api_router

app = FastAPI(
    title="Meetup Clone",
    openapi_url="/api/v1/openapi.json"
)

app.include_router(api_router, prefix="/api/v1")

auth_scheme = HTTPBearer()


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")

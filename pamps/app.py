from fastapi import FastAPI
from pamps.config import settings

from .routes import main_router

app = FastAPI(
    title="Pamps",
    version="0.1.0",
    description="Pamps is a posting app to clone twitter",
    openapi_url=f"{settings.version_api.VERSION_API_STR}/openapi.json",
)
app.include_router(
    main_router,
    prefix=settings.version_api.VERSION_API_STR
)
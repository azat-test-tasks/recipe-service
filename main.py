from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.api_v1.api import api_router as api_router_v1
from core.config import settings
from core.logging import register_logs

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    docs_url=settings.API_V1_STR + "/docs",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

logger = register_logs(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router_v1, prefix=settings.API_V1_STR)

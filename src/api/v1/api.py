from fastapi import APIRouter
from api.v1.endpoints import ma

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(ma.router, prefix="/ma")

from fastapi import APIRouter

from .base import base_router
from .users import users_router

v1_router = APIRouter()
v1_router.include_router(users_router)
v1_router.include_router(base_router)

from fastapi import APIRouter

from app.core import dependency

from .users import router

users_router = APIRouter()
# users_router.include_router(router, prefix="/user", tags=["用户模块"], dependencies=[dependency.judge_authed])

users_router.include_router(router, prefix="/user", tags=["用户模块"], dependencies=[])

__all__ = ["users_router"]

from fastapi import APIRouter

from .user import user_router
from .auth import token_router
from .post import post_router

main_router = APIRouter()

main_router.include_router(token_router, tags=["auth"])
main_router.include_router(user_router, prefix="/user", tags=["user"])
main_router.include_router(post_router, prefix="/post", tags=["post"])
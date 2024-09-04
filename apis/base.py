from fastapi import APIRouter

from apis.v1 import route_user, router_book


api_router = APIRouter()
api_router.include_router(route_user.router, prefix="", tags=["users"])
api_router.include_router(router_book.router, prefix="", tags=["books"])

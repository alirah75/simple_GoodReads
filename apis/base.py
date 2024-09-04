from fastapi import APIRouter

from apis.v1 import route_user, router_book, router_bookmark, router_comment, router_rating


api_router = APIRouter()
api_router.include_router(route_user.router, prefix="", tags=["users"])
api_router.include_router(router_book.router, prefix="", tags=["books"])
api_router.include_router(router_bookmark.router, prefix="", tags=["bookmark"])
api_router.include_router(router_comment.router, prefix="", tags=["comment"])
api_router.include_router(router_rating.router, prefix="", tags=["rating"])

from fastapi import APIRouter
from apis import route_books
from apis import route_login
from apis import route_users


api_router = APIRouter()
api_router.include_router(route_users.router, prefix="/users", tags=["users"])
api_router.include_router(route_books.router, prefix="/books", tags=["books"])
api_router.include_router(route_login.router, prefix="/login", tags=["login"])

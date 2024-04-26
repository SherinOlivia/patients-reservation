from fastapi import APIRouter
from v1.endpoints import users

router = APIRouter()

router.include_router(users.userRouter, prefix="/users", tags=["users"])

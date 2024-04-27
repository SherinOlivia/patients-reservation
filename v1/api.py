from fastapi import APIRouter
from v1.endpoints import doctors, users

router = APIRouter()

router.include_router(users.userRouter, prefix="/users", tags=["users"])
router.include_router(doctors.doctorRouter, prefix="/doctors", tags=["doctors"])
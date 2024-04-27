from fastapi import APIRouter
from v1.endpoints import doctors, schedules, users

router = APIRouter()

router.include_router(users.userRouter, prefix="/users", tags=["users"])
router.include_router(doctors.doctorRouter, prefix="/doctors", tags=["doctors"])
router.include_router(schedules.scheduleRouter, prefix="/schedules", tags=["schedules"])
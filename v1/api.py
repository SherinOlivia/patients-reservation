from fastapi import APIRouter
from v1.endpoints import doctors, reservations, schedules, users

router = APIRouter()

router.include_router(users.userRouter, prefix="/users", tags=["Users"])
router.include_router(doctors.doctorRouter, prefix="/doctors", tags=["Doctors"])
router.include_router(schedules.scheduleRouter, prefix="/schedules", tags=["Schedules"])
router.include_router(reservations.reservationRouter, prefix="/reservations", tags=["Reservations"])
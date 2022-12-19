from fastapi import APIRouter

from api.file import router as files_router
from api.users import router as users_router

router = APIRouter()
router.include_router(files_router)
router.include_router(users_router)

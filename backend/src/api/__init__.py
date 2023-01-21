from fastapi import APIRouter
from .auth import router as auth_router
from .posts import router as posts_router
from .like import router as like_router


router = APIRouter()

router.include_router(auth_router)
router.include_router(posts_router)
router.include_router(like_router)

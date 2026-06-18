from app.api.v1.x.accounts import router as accounts_router
from app.api.v1.x.posts import router as posts_router
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/x")
router.include_router(accounts_router)
router.include_router(posts_router)

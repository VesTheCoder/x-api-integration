from app.api.v1.x.accounts import router as accounts_router
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/x")
router.include_router(accounts_router)

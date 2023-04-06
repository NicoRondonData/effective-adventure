from fastapi import APIRouter, Depends

from app.auth.services import register_user_service, login_user_service, logout_service

router = APIRouter(prefix="/api")


@router.get("/livez")
async def liveness_probe():
    return {"liveness": "True"}

@router.post("/auth/login")
async def login(response: dict = Depends(login_user_service)):
    return response


@router.post("/auth/logout")
async def logout(response: dict = Depends(logout_service)):
    return response


@router.post("/auth/register")
async def register(response: dict = Depends(register_user_service)):
    return response

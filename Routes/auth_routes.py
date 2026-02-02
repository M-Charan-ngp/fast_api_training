from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from Config.database import get_db
from Controllers import auth_controller
from Middlewares.auth_key_middleware import validate_auth_key
from schemas import user as user_schema

router = APIRouter(
    tags=["Authentication"],
    dependencies=[Depends(validate_auth_key)]
    )

@router.post("/register")
async def register(user_in: user_schema.UserCreate, db: AsyncSession = Depends(get_db)):
    print("inside route")
    user = await auth_controller.register_new_user(db, user_in)
    if not user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {
        "status":"success",
        "msg":"Registration Success"
    }

@router.post("/login")
async def login(form_data: user_schema.LoginRequest, db: AsyncSession = Depends(get_db)):
    token = await auth_controller.login_user(db, form_data.username, form_data.password)
    if not token:
        return "Invalid Credentials"
    return {
        "token":token,
        "type":"Bearer"
    }
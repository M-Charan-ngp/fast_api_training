from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from Config.database import get_db
from Models.User import UserModel, UserRole
from Utils.auth import verify_token

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> UserModel:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Authorization Header")
    
    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    query = await db.execute(select(UserModel).where(UserModel.username == payload.get("name")))
    user = query.scalars().first()
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

class RoleChecker:
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: UserModel = Depends(get_current_user)):
        print(current_user.role.value)
        if current_user.role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Don't have permission to access this route")
        return current_user
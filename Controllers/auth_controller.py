from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from Models.User import UserModel
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from schemas.user import UserCreate
from Utils.security import hash_password, verify_password
from Utils.auth import create_token

async def register_new_user(db: AsyncSession, user_data: UserCreate):
    try:

        hashed_pwd = hash_password(user_data.password)
        new_user = UserModel(
            username=user_data.username,
            password_hash=hashed_pwd,
            role = user_data.role.value
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    except Exception as e:
        await db.rollback()
        print(f"Registration Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )

async def login_user(db: AsyncSession, username, password):
    try:
        query = await db.execute(select(UserModel).where(UserModel.username == username))
        user = query.scalars().first()
        if user and verify_password(password, user.password_hash):
            token = create_token({"name": user.username, "role": user.role.value})
            return token
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Login Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )
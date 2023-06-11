from fastapi import APIRouter, Depends, UploadFile, File
from fastapi_users import FastAPIUsers
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import auth_backend
from src.auth.database import get_async_session
from src.auth.manager import get_user_manager
from src.api.schemas import CreateProfile, UpdateProfile
from models.models import profile, User

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user()


router = APIRouter(prefix="/acc", tags=["Account"])


@router.get("/")
async def get_profile(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    try:
        query = select(profile).where(profile.c.user_id == user.id)
        result = await session.execute(query)
        profiles = result.scalars().all()
        return {"status": "success", "result": profiles}
    except SQLAlchemyError as e:
        error_message = "Произошла ошибка при выполнении запроса."
        return {"error": error_message, "details": str(e)}
    except Exception as e:
        error_message = "Произошла непредвиденная ошибка."
        return {"error": error_message, "details": str(e)}


@router.post("/create")
async def create_profile(
    avatar: UploadFile = File(default=None),
    new_profile: CreateProfile = Depends(),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    try:
        new_profile_dict = new_profile.dict()
        if avatar is None:
            new_profile_dict["avatar_url"] = "avatars/default.png"
        else:
            file_path = f"avatars/{avatar.filename}"
            with open(file_path, "wb") as file:
                contents = await avatar.read()
                file.write(contents)

            new_profile_dict["avatar_url"] = file_path
        new_profile_dict["user_id"] = user.id
        stmt = insert(profile).values(**new_profile_dict)
        print(new_profile.dict())
        await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    except SQLAlchemyError as e:
        error_message = "Произошла ошибка при выполнении запроса."
        return {"error": error_message, "details": str(e)}
    except Exception as e:
        error_message = "Произошла непредвиденная ошибка."
        return {"error": error_message, "details": str(e)}


@router.delete("/delete")
async def delete_profile(
    profile_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    try:
        is_user_id = select(profile.c.id).where(profile.c.user_id == user.id)
        result = await session.execute(is_user_id)
        rows = [row[0] for row in result.fetchall()]
        if profile_id in rows:
            stmt = delete(profile).where(profile_id == profile.c.id)
            await session.execute(stmt)
            await session.commit()
            return {"status": "success"}
        else:
            return {"status": "error", "details": "Missing ID"}
    except SQLAlchemyError as e:
        error_message = "Произошла ошибка при выполнении запроса."
        return {"error": error_message, "details": str(e)}
    except Exception as e:
        error_message = "Произошла непредвиденная ошибка."
        return {"error": error_message, "details": str(e)}


@router.put("/update")
async def update_profile(
    profile_id: int,
    new_profile: UpdateProfile = Depends(),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    try:
        is_user_id = select(profile.c.id).where(profile.c.user_id == user.id)
        result = await session.execute(is_user_id)
        rows = [row[0] for row in result.fetchall()]
        if profile_id in rows:
            stmt = (
                update(profile)
                .where(profile_id == profile.c.id)
                .values(**new_profile.dict())
            )
            await session.execute(stmt)
            await session.commit()
            return {"status": "success"}
        else:
            return {"status": "error", "details": "Missing ID"}
    except SQLAlchemyError as e:
        error_message = "Произошла ошибка при выполнении запроса."
        return {"error": error_message, "details": str(e)}
    except Exception as e:
        error_message = "Произошла непредвиденная ошибка."
        return {"error": error_message, "details": str(e)}

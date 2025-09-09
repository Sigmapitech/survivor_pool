from fastapi import APIRouter, Depends, HTTPException, status
from passlib.hash import bcrypt
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..crud.users import (
    delete_user,
    get_user,
    get_user_by_email,
    get_users,
    patch_user,
    update_user,
)
from ..db import get_session
from ..helpers.caching_proxy import cached_endpoint, cached_list_endpoint, get_image
from ..jeb_schema import UserBase
from ..models import User
from ..proxy_schema import Message
from ..schemas.users import PatchRequest, UpdateRequest

router = APIRouter()


@cached_list_endpoint("/users", db_model=User, pydantic_model=UserBase)
async def route_list_users(db: AsyncSession = Depends(get_session), skip=0, limit=100):
    return await get_users(db, skip, limit)


@cached_endpoint("/users/{user_id}", db_model=User, pydantic_model=UserBase)
async def route_read_user_by_id(user_id: int, db: AsyncSession = Depends(get_session)):
    return await get_user(db, user_id)


@get_image("/users/{user_id}/image")
async def route_get_user_image(
    user_id: int,
): ...  # The decorator does all so no need to complete this


@cached_endpoint("/users/email/{email}", db_model=User, pydantic_model=UserBase)
async def route_read_user_by_mail(
    email: EmailStr, db: AsyncSession = Depends(get_session)
):
    return await get_user_by_email(db, email)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete user",
    responses={
        404: {"model": Message, "description": "User not found"},
    },
)
async def route_delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    return await delete_user(db, user_id)


@router.put(
    "/{user_id}",
    response_model=UserBase,
    description="Update user",
    responses={
        404: {"model": Message, "description": "User not found"},
        200: {"model": UserBase, "description": "User updated"},
        400: {"model": Message, "description": "email already in use"},
    },
)
async def route_update_user(
    user_id: int, data: UpdateRequest, db: AsyncSession = Depends(get_session)
) -> UserBase:
    return await update_user(db, user_id, data)


@router.patch(
    "/{user_id}",
    response_model=UserBase,
    description="Patch user",
    responses={
        404: {"model": Message, "description": "User not found"},
        200: {"model": UserBase, "description": "User patched"},
        400: {"model": Message, "description": "email already in use"},
    },
)
async def route_patch_user(
    user_id: int, data: PatchRequest, db: AsyncSession = Depends(get_session)
) -> UserBase:
    return await patch_user(db, user_id, data)

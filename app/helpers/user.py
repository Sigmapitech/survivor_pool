from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..endpoints.auth import decode_access_token
from ..models import User


def get_user_id_from_token(authorization: str) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No token, authorization denied")

    token = authorization.split(" ")[1]
    payload = decode_access_token(token)

    id = payload.get("id")
    if not id:
        raise HTTPException(status_code=401, detail="Token is not valid")
    return id


async def get_user_from_token(db: AsyncSession, authorization: str) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No token, authorization denied")

    token = authorization.split(" ")[1]
    payload = decode_access_token(token)

    id = payload.get("id")
    if not id:
        raise HTTPException(status_code=401, detail="Token is not valid")

    result = await db.execute(select(User).filter(User.id == id))
    user = result.scalar()
    if not user:
        raise HTTPException(404, detail="User not found from token")
    return user

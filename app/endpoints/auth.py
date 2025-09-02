from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, Depends, HTTPException
from passlib.hash import bcrypt
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..config import settings
from ..db import get_session
from ..models import User

router = APIRouter()

ACCES_TOKEN_TIMEOUT = 42


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.jwt_secret)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCES_TOKEN_TIMEOUT)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret)
    return encoded_jwt


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: str


class AuthResponse(BaseModel):
    token: str


@router.post(
    "/register/",
    response_model=AuthResponse,
    description="Register a new user",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": AuthResponse(
                        token=create_access_token(
                            {"id": 1, "email": "www.xxx@yyyy.zzz"}, timedelta(0)
                        )
                    ).model_dump()
                }
            },
        },
        400: {
            "content": {
                "application/json": {"example": {"detail": "Account already exists"}}
            },
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {"loc": ["string", 0], "msg": "string", "type": "string"}
                        ]
                    }
                }
            },
        },
    },
)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_session)):
    # TODO: Setup mail verification via SMTP
    result = await db.execute(select(User).filter(User.email == data.email))
    collected = result.scalars().all()
    if len(collected) > 0:
        raise HTTPException(status_code=400, detail="Account already exists")

    user = User(
        auth=bcrypt.hash(data.password),
        email=data.email,
        name=data.name,
        role=data.role,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token({"id": user.id, "email": user.email})
    return AuthResponse(token=token)


@router.post(
    "/login/",
    response_model=AuthResponse,
    description="Login with account",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": AuthResponse(
                        token=create_access_token(
                            {"id": 1, "email": "www.xxx@yyyy.zzz"}, timedelta(0)
                        )
                    ).model_dump()
                }
            },
        },
        401: {
            "content": {
                "application/json": {"example": {"detail": "Invalid Credentials"}}
            },
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {"loc": ["string", 0], "msg": "string", "type": "string"}
                        ]
                    }
                }
            },
        },
    },
)
async def login(
    data: LoginRequest, db: AsyncSession = Depends(get_session)
) -> AuthResponse:
    result = await db.execute(select(User).filter(User.email == data.email))
    user = result.scalars().first()
    if not user or not bcrypt.verify(data.password, str(user.auth)):
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    token = create_access_token({"id": user.id, "email": user.email})
    return AuthResponse(token=token)

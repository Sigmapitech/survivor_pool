import logging
import re
import secrets
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, Header, HTTPException
from jinja2 import Template
from passlib.hash import bcrypt
from pydantic import BaseModel, EmailStr, StringConstraints
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..config import settings
from ..db import get_session
from ..helpers.mail import EmailSchema, send_email
from ..models import User
from ..proxy_schema import Message

router = APIRouter()
logger = logging.getLogger(__name__)

ACCES_TOKEN_TIMEOUT = 42
ALGORITHM = "HS256"

type PasswordStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=8,
        max_length=50,
        pattern=re.compile(
            r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        ),
    ),
]


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid token {e}")
        raise HTTPException(status_code=401, detail="Invalid token")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCES_TOKEN_TIMEOUT)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=ALGORITHM)
    return encoded_jwt


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: PasswordStr
    name: str
    role: str


class VerificationRequest(BaseModel):
    code: int


class AuthResponse(BaseModel):
    token: str


@router.post("/verify/")
async def verify_user(
    data: VerificationRequest,
    db: AsyncSession = Depends(get_session),
    authorization: str = Header(None),
) -> Message:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No token, authorization denied")

    token = authorization.split(" ")[1]
    payload: dict[str, int] = decode_access_token(token)
    result = await db.execute(select(User).where(User.id == payload.get("id")))
    user = result.scalar()
    if user is None:
        raise HTTPException(404, detail="User not found")
    logger.warning(user.verification_code, data.code)
    if getattr(user, "verification_code", None) != data.code:
        raise HTTPException(400, "Verification code is incorrect")
    setattr(user, "verified_email", True)
    await db.commit()
    return Message(message="Properly verified")


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
    result = await db.execute(select(User).filter(User.email == data.email))
    collected = result.scalars().all()
    if len(collected) > 0:
        raise HTTPException(status_code=400, detail="Account already exists")

    code = secrets.randbelow(10**6)
    user = User(
        auth=bcrypt.hash(data.password),
        email=data.email,
        name=data.name,
        role=data.role,
        verified_email=False,
        verification_code=code,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token({"id": user.id, "email": user.email})
    with open("app/templates/auth_verification.html") as file:
        template_str = file.read()

    jinja_template: Template = Template(template_str)
    body = jinja_template.render(
        verification_url=f"http://localhost:8000/api/auth/verify/",
        verification_code=str(code).zfill(6),
        current_year=datetime.now(timezone.utc).year,
    )

    await send_email(
        EmailSchema(
            to=str(user.email),
            subject="Votre compte JEB - Confirmation de votre adresse mail",
            body=body,
        ),
        content_type="html",
    )
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

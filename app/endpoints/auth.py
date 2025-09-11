import logging
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, Depends, Header, HTTPException
from jinja2 import Template
from passlib.hash import bcrypt
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..config import settings
from ..db import get_session
from ..helpers.mail import EmailSchema, send_email
from ..models import User
from ..proxy_schema import Message
from ..schemas.users import PasswordStr

router = APIRouter()
logger = logging.getLogger(__name__)

ACCES_TOKEN_TIMEOUT = 42
ALGORITHM = "HS256"


def decode_access_token(token: str):
    """
    Decodes a JWT access token and returns its payload.

    Args:
        token (str): The JWT access token to decode.

    Returns:
        dict: The decoded payload from the JWT token.

    Raises:
        HTTPException: If the token has expired or is invalid.
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid token {e}")
        raise HTTPException(status_code=401, detail="Invalid token")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Creates a JWT access token with an expiration time.

    Args:
        data (dict): The payload data to include in the token.
        expires_delta (timedelta, optional): The time duration after which the token will expire. Defaults to None.

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCES_TOKEN_TIMEOUT)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=ALGORITHM)
    return encoded_jwt


async def get_user_from_token(db: AsyncSession, authorization: str):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No token, authorization denied")

    token = authorization.split(" ")[1]
    payload: dict[str, int] = decode_access_token(token)
    id = payload.get("id")
    if not id:
        raise HTTPException(status_code=401, detail="Token is not valid")
    result = await db.execute(select(User).where(User.id == id))
    user = result.scalar()
    if user is None:
        raise HTTPException(404, detail="User not found")
    return user


def get_user_id_from_token(authorization: str) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No token, authorization denied")

    token = authorization.split(" ")[1]
    payload = decode_access_token(token)

    id = payload.get("id")
    if not id:
        raise HTTPException(status_code=401, detail="Token is not valid")
    return id


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: PasswordStr
    name: str


class VerificationRequest(BaseModel):
    code: int


class AuthResponse(BaseModel):
    token: str


@router.post(
    "/verify/",
    response_model=Message,
    description="Verify user account",
    responses={
        200: {"model": Message, "description": "User verified"},
        400: {"model": Message, "description": "Verification code is incorrect"},
        401: {"model": Message, "description": "No token, authorization denied"},
        404: {"model": Message, "description": "User not found"},
    },
)
async def verify_user(
    data: VerificationRequest,
    db: AsyncSession = Depends(get_session),
    authorization: str = Header(None),
) -> Message:
    user = await get_user_from_token(db, authorization)
    if getattr(user, "verification_code", None) != data.code:
        raise HTTPException(400, "Verification code is incorrect")
    setattr(user, "verified_email", True)
    await db.commit()
    return Message(message="Properly verified")


async def is_verified(
    db: AsyncSession = Depends(get_session),
    authorization: str = Header(None),
):
    user = await get_user_from_token(db, authorization)
    return getattr(user, "verified_email") == True


PERMS = ("STARTUP", "ADMIN", "USER")


def as_enough_perms(perm: str, user: User):
    user_role = getattr(user, "role")
    return user_role == "ADMIN" or user_role == perm


@router.post(
    "/register/",
    response_model=AuthResponse,
    description="Register a new account",
    status_code=201,
    responses={
        201: {"model": AuthResponse, "description": "Account created"},
        400: {"model": Message, "description": "Account already exists"},
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
    "/resend",
)
async def resend_verification_code(
    db: AsyncSession = Depends(get_session), authorization: str = Header(None)
):
    user = await get_user_from_token(db, authorization)
    code = secrets.randbelow(10**6)

    with open("app/templates/auth_verification.html") as file:
        template_str = file.read()

    jinja_template: Template = Template(template_str)
    body = jinja_template.render(
        verification_url=f"http://localhost:8000/api/auth/verify/",
        verification_code=str(code).zfill(6),
        current_year=datetime.now(timezone.utc).year,
    )

    setattr(user, "verification_code", code)
    await db.commit()
    await send_email(
        EmailSchema(
            to=getattr(user, "email"),
            subject="Votre compte JEB - Confirmation de votre adresse mail",
            body=body,
        ),
        content_type="html",
    )
    return Message(message="Mail resent correctly")


@router.post(
    "/login/",
    response_model=AuthResponse,
    description="Login with account",
    responses={
        200: {"model": AuthResponse, "description": "Login successful"},
        401: {"model": Message, "description": "Invalid Credentials"},
    },
)
async def login(
    data: LoginRequest, db: AsyncSession = Depends(get_session)
) -> AuthResponse:
    result = await db.execute(select(User).filter(User.email == data.email))
    user = result.scalars().first()
    if not user or not bcrypt.verify(data.password, str(user.authentication_string)):
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    token = create_access_token({"id": user.id, "email": user.email})
    return AuthResponse(token=token)

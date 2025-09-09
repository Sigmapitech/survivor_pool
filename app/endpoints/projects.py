import hashlib
import os
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Header,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.users import User

from ..db import get_session
from ..helpers.user import get_user_id_from_token
from ..jeb_schema import UserBase
from ..models import Project
from ..models.startups import Startup
from ..proxy_schema import Message, ProjectBase

router = APIRouter()

ALLOWED_IMAGE_TYPES = {
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/gif",
    "image/webp",
}
CONTENT_TYPE_TO_EXT = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/gif": ".gif",
    "image/webp": ".webp",
}


def build_image_path(name: str, description: str, logo: UploadFile | None) -> Path:
    base = hashlib.sha256((name + description).encode()).hexdigest()
    if logo and logo.content_type in CONTENT_TYPE_TO_EXT:
        ext = CONTENT_TYPE_TO_EXT[logo.content_type]
        return CACHE_DIR / f"{base}{ext}"
    return CACHE_DIR / base


CACHE_DIR = Path("app/static/images")
os.makedirs(CACHE_DIR, exist_ok=True)


def validate_image(logo: UploadFile | None):
    if logo and logo.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            400,
            detail=f"Unsupported file type: {logo.content_type}. Allowed: {', '.join(ALLOWED_IMAGE_TYPES)}",
        )


@router.get(
    "/",
    response_model=list[ProjectBase],
    description="List all projects",
    responses={
        200: {"model": list[ProjectBase], "description": "List of projects"},
    },
)
async def list_project(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Project).options(selectinload(Project.liked_by)))
    return [
        ProjectBase(
            logo=getattr(project, "logo"),
            name=getattr(project, "name"),
            descritpion=getattr(project, "description"),
            worth=getattr(project, "worth"),
            nugget=len(project.liked_by),
        )
        for project in result.scalars().all()
    ]


@router.get(
    "/{project_id}",
    response_model=ProjectBase,
    description="Get a project by ID",
    responses={
        200: {"model": ProjectBase, "description": "Project found"},
        404: {"model": Message, "description": "Project not found"},
    },
)
async def read_project(project_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(Project)
        .filter(Project.id == project_id)
        .options(selectinload(Project.liked_by))
    )
    collected = result.scalars().first()
    if not collected:
        raise HTTPException(404, detail="Not Found")
    return ProjectBase(**collected, nugget=len(collected.liked_by))


@router.get(
    "/{project_id}/investors",
    response_model=list[UserBase],
    description="List investors of a project",
    responses={
        200: {"model": list[UserBase], "description": "List of investors"},
        404: {"model": Message, "description": "Project not found"},
    },
)
async def list_project_investors(
    project_id: int, db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(Project).filter(Project.id == project_id).join(Project.investors)
    )
    return result.scalars().all()


@router.post(
    "/{startup_id}",
    response_model=Message,
    status_code=status.HTTP_201_CREATED,
    description="Create a new project for a startup",
    responses={
        201: {"model": Message, "description": "Project successfully created"},
        400: {
            "model": Message,
            "description": "A project with the same name and description already exist",
        },
        404: {"model": Message, "description": "Startup not found"},
    },
)
async def create_project(
    startup_id: int,
    logo: UploadFile | None = File(None),
    name: str = Form(...),
    description: str = Form(...),
    db: AsyncSession = Depends(get_session),
) -> Message:
    validate_image(logo)
    ressult = await db.execute(select(Startup).filter(Startup.id == startup_id))
    startup = ressult.scalar()
    if not startup:
        raise HTTPException(404, detail="Startup not found")
    filepath = build_image_path(name, description, logo)
    if filepath.exists():
        raise HTTPException(
            400, detail="A project with the same name and description already exist"
        )
    if logo:
        with filepath.open("wb") as f:
            data = await logo.read()
            f.write(data)
    project = Project(
        logo=str(filepath),
        name=name,
        description=description,
        worth=0,
        startup_id=startup_id,
    )
    db.add(project)
    await db.commit()
    return Message(message="Project successfully created")


@router.put(
    "/{project_id}",
    response_model=Message,
    description="Update a project",
    responses={
        200: {"model": Message, "description": "Project successfully updated"},
        404: {"model": Message, "description": "Project not found"},
    },
)
async def update_project(
    project_id: int,
    name: str = Form(...),
    description: str = Form(...),
    logo: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_session),
) -> Message:
    validate_image(logo)
    result = await db.execute(select(Project).filter(Project.id == project_id))
    project = result.scalar()
    if not project:
        raise HTTPException(404, detail="Project not found")
    old_filepath = getattr(project, "logo")
    new_filepath = build_image_path(name, description, logo)
    if logo:
        if old_filepath:
            os.remove(getattr(project, "logo"))
        with new_filepath.open("wb") as f:
            data = await logo.read()
            f.write(data)
        setattr(project, "logo", str(new_filepath))
    elif old_filepath:
        os.rename(old_filepath, new_filepath)
        setattr(project, "logo", str(new_filepath))
    setattr(project, "name", name)
    setattr(project, "description", description)
    await db.commit()
    return Message(message="Project successfully updated")


@router.patch(
    "/{project_id}",
    response_model=Message,
    description="Patch a project",
    responses={
        200: {"model": Message, "description": "Project successfully updated"},
        404: {"model": Message, "description": "Project not found"},
    },
)
async def patch_project(
    project_id: int,
    name: str | None = Form(None),
    description: str | None = Form(None),
    logo: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_session),
) -> Message:
    validate_image(logo)
    result = await db.execute(select(Project).filter(Project.id == project_id))
    project = result.scalar()
    if not project:
        raise HTTPException(404, detail="Project not found")
    if name:
        setattr(project, "name", name)
    if description:
        setattr(project, "description", description)

    if logo:
        new_filepath = build_image_path(
            name or getattr(project, "name"),
            description or getattr(project, "description"),
            logo,
        )
        if getattr(project, "logo"):
            os.remove(getattr(project, "logo"))
        with new_filepath.open("wb") as f:
            data = await logo.read()
            f.write(data)
        setattr(project, "logo", str(new_filepath))
    await db.commit()
    return Message(message="Project successfully updated")


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a project",
    responses={
        404: {"model": Message, "description": "Project not found"},
    },
)
async def delete_project(project_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Project).filter(Project.id == project_id))
    project = result.scalar()
    if not project:
        raise HTTPException(404, detail="Project not found")
    await db.delete(project)
    await db.commit()


@router.post(
    "/{project_id}/like",
    response_model=Message,
    description="Like a project",
    responses={
        200: {"model": Message, "description": "Project liked"},
        400: {"model": Message, "description": "Already liked"},
        404: {"model": Message, "description": "User or Project not found"},
    },
)
async def like_project(
    project_id: int,
    db: AsyncSession = Depends(get_session),
    authorization: str = Header(None),
) -> Message:
    user_id = get_user_id_from_token(authorization)
    result = await db.execute(
        select(User)
        .filter(User.id == user_id)
        .options(selectinload(User.liked_projects))
    )
    user = result.scalar()
    if not user:
        raise HTTPException(404, "User not found")

    result = await db.execute(select(Project).filter(Project.id == project_id))
    project = result.scalar()
    if not project:
        raise HTTPException(404, "Project not found")

    if project in user.liked_projects:
        raise HTTPException(400, detail="Already liked")
    user.liked_projects.append(project)
    await db.commit()
    return Message(message="Project liked")

import hashlib
import os
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, Header, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.users import User

from ..db import get_session
from ..helpers.user import get_user_id_from_token
from ..models import Project
from ..models.startups import Startup
from ..proxy_schema import Message, ProjectBase
from ..jeb_schema import UserBase

router = APIRouter()

CACHE_DIR = Path("app/static/images")
os.makedirs(CACHE_DIR, exist_ok=True)


@router.get("/", response_model=list[ProjectBase])
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


@router.get("/{project_id}", response_model=ProjectBase)
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


@router.get("/{project_id}/investors")
async def list_project_investors(
    project_id: int, db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(Project).filter(Project.id == project_id).join(Project.investors)
    )
    return result.scalars().all()


@router.post("/{startup_id}", response_model=Message)
async def create_project(
    startup_id: int,
    logo: UploadFile | None = File(None),
    name: str = Form(...),
    description: str = Form(...),
    db: AsyncSession = Depends(get_session),
) -> Message:
    ressult = await db.execute(select(Startup).filter(Startup.id == startup_id))
    startup = ressult.scalar()
    if not startup:
        raise HTTPException(404, detail="Startup not found")
    filepath = CACHE_DIR / (
        f"{hashlib.sha256((name + description).encode()).hexdigest()}"
    )
    if filepath.exists():
        raise HTTPException(
            400, detail="A project with the same name and description already exist"
        )
    if logo:
        with filepath.open("w+") as f:
            data = await logo.read()
            f.write(str(data))
    project = Project(
        logo=str(filepath),
        name=name,
        description=description,
        worth=0,
        startup_id=startup_id,
    )
    db.add(project)
    await db.commit()
    return Message(message="Project successfuly created")


@router.post("/{project_id}/like", response_model=Message)
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

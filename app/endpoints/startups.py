from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_startup():
    return {}


@router.get("/{startup_id}")
async def read_startup(startup_id: int):
    return {}


@router.get("/{startup_id}/founders/{founder_id}/image")
async def read_founder_image(startup_id: int, founder_id: int):
    return {}

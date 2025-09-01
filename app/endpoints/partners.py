from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_partners():
    return {}


@router.get("/{partners_id}")
async def read_partners(partners_id: int):
    return {}

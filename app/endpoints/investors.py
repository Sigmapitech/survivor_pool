from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_investor():
    return {}


@router.get("/{investor_id}")
async def read_investor(investor_id: int):
    return {}

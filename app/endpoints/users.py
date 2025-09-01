from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_user():
    return {}


@router.get("/{user_id}")
async def read_user_by_id(user_id: int):
    return {}


@router.get("/{user_id}/image")
async def get_user_image(user_id: int):
    return {}


@router.get("/email/{email}")
async def read_user_by_mail(email):
    return {}

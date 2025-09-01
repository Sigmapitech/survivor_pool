from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_event():
    return {}


@router.get("/{event_id}")
async def read_event(event_id: int):
    return {}


@router.get("/{event_id}/image")
async def get_event_image(event_id: int):
    return {}

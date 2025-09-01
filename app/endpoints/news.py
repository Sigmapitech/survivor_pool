from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_news():
    return {}


@router.get("/{news_id}")
async def read_news(news_id: int):
    return {}


@router.get("/{news_id}/image")
async def get_news_image(news_id: int):
    return {}

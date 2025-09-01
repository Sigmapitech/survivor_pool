import importlib

from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse

from ..proxy_schema import Message

router = APIRouter()


@router.get(
    "/api/",
    response_model=Message,
    description="API root to test API response",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": Message(message="Hello, World!").model_dump()
                }
            },
        }
    },
)
async def hello_world():
    return JSONResponse(content={"message": "Hello, World!"})


def register_all(app: FastAPI):
    app.include_router(router)
    for module in ("events", "investors", "news", "partners", "startups", "users"):
        mod = importlib.import_module(f".{module}", package="app.endpoints")
        app.include_router(mod.router, prefix=f"/api/{module}", tags=[f"{module}"])


__all__ = ("register_all",)

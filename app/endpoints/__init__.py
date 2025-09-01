import importlib

from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/api/")
async def hello_world():
    return JSONResponse(content={"message": "Hello, World!"})


def register_all(app: FastAPI):
    app.include_router(router)
    for module in ("events", "investors", "news", "partners", "startups", "users"):
        mod = importlib.import_module(f".{module}", package="app.endpoints")
        app.include_router(mod.router, prefix=f"/api/{module}")


__all__ = ("register_all",)

from http import HTTPStatus
import uvicorn
from starlette.exceptions import HTTPException as StarletteHTTPException

import os
import logging
import sys
from contextlib import asynccontextmanager

from starlette.responses import FileResponse, JSONResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from . import endpoints
from .db import init_db

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan, redoc_url="/api/doc", docs_url=None)

if "dev" in sys.argv:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=("http://localhost" "http://127.0.0.1:*"),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.mount("/", StaticFiles(directory="front/dist", html=True), name="dist")

endpoints.register_all(app)


def log_routes(app: FastAPI):
    data = sorted(app.routes, key=lambda r: r.path)
    for route in data:
        if hasattr(route, "methods"):
            methods = ", ".join(route.methods)
            logger.info(f"{methods:>10} -> {route.path}")


log_routes(app)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


# v- fixup for prod serve:


@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request, exc: StarletteHTTPException):
    if exc.status_code == HTTPStatus.NOT_FOUND.value:
        if request.url.path.startswith("/api/"):
            return JSONResponse(
                status_code=HTTPStatus.NOT_FOUND.value,
                content={"detail": "API endpoint not found"},
            )

        index_file = os.path.join("front/dist", "index.html")
        return FileResponse(index_file)

    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


def main():
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()

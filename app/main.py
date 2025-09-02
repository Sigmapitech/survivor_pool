import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


endpoints.register_all(app)


def log_routes(app: FastAPI):
    data = sorted(app.routes, key=lambda r: r.path)
    for route in data:
        if hasattr(route, "methods"):
            methods = ", ".join(route.methods)
            logger.info(f"{methods:>10} -> {route.path}")


log_routes(app)


# do not inverse mounting points!
# app.mount("/uploads", StaticFiles(directory="assets/uploads"), name="uploads")


def main():
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()

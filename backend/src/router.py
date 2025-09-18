from fastapi import FastAPI, APIRouter

from src.settings import settings

from src.apps.asm.router import router as asm_router


def apply_routes(app: FastAPI) -> FastAPI:
    # API V1 router
    router_v1 = APIRouter(prefix=settings.api.v1.prefix)

    # Include API V1 routers
    router_v1.include_router(asm_router)

    # Include API V1 router
    app.include_router(router_v1)
    return app

from contextlib import asynccontextmanager

import gradio as gr
from fastapi import FastAPI

from app.agents.me_agent import MeAgent
from app.api.chat_routes import router as chat_router
from app.config.settings import settings
from app.core.exception_handlers import register_exception_handlers
from app.core.health import check_qdrant, check_redis
from app.core.logging import setup_logging
from app.infrastructure.qdrant_client import client as qdrant_client
from app.infrastructure.redis_client import redis
from app.services.factory import build_rag_service
from app.services.history_store import RedisHistoryStore
from app.services.session import SessionService
from app.ui.gradio_app import create_gradio_app


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    check_redis(redis)
    check_qdrant(qdrant_client)

    rag_service = build_rag_service()

    app.state.agent = MeAgent(rag_service=rag_service)
    app.state.session_service = SessionService()
    app.state.history_store = RedisHistoryStore(redis)

    yield


app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    responses={422: {"description": "Disabled — replaced by 400 VALIDATION_ERROR"}},
    lifespan=lifespan,
)

register_exception_handlers(app)

# API routes
app.include_router(chat_router)

# Gradio UI
gradio_app = create_gradio_app(lambda: app.state.agent)

app = gr.mount_gradio_app(app, gradio_app, path="/")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        reload=not settings.is_production,
        log_level=settings.log_level.lower(),
    )

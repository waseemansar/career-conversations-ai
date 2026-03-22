from typing import Callable

import gradio as gr
from loguru import logger

from app.agents.me_agent import MeAgent
from app.config.settings import settings


def create_gradio_app(get_agent: Callable[[], MeAgent]) -> gr.ChatInterface:
    def chat_handler(*args, **kwargs):
        try:
            return get_agent().chat(*args, **kwargs)
        except Exception as e:
            logger.error(f"Chat handler error: {e}")
            raise gr.Error("Something went wrong. Please try again.")

    return gr.ChatInterface(
        fn=chat_handler,
        title=settings.app_name,
        chatbot=gr.Chatbot(
            value=[{"role": "assistant", "content": settings.welcome_message}],
            avatar_images=(None, settings.avatar_path)
            if settings.avatar_path
            else None,
        ),
    )

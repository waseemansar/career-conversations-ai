import json
from typing import Any, Dict, List

from loguru import logger

from app.config.settings import settings
from app.core.exceptions import OpenAIError
from app.infrastructure.openai_client import openai
from app.services.rag import RAGService
from app.tools.notifications import TOOL_FUNCTIONS, tools


class MeAgent:
    def __init__(self, rag_service: RAGService) -> None:
        self.openai = openai
        self.name = settings.app_owner
        self.rag_service = rag_service

    def _build_system_prompt(self) -> str:
        return (
            f"You are acting as {self.name}. You are answering questions on {self.name}'s website, "
            f"particularly questions related to {self.name}'s career, background, skills and experience. "
            f"Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. "
            "Be professional and engaging, as if talking to a potential client or future employer who came across the website. "
            "If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, "
            "even if it's about something trivial or unrelated to career. "
            "If the user is engaging in discussion, try to steer them towards getting in touch via email; "
            "ask for their email and record it using your record_user_details tool. "
            "Use any background information provided about Waseem's career and LinkedIn profile to ground your answers in factual details."
        )

    def _handle_tool_calls(self, tool_calls: List[Any]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []

        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            tool = TOOL_FUNCTIONS.get(tool_name)
            result = tool(**arguments)

            results.append(
                {
                    "role": "tool",
                    "content": json.dumps(result),
                    "tool_call_id": tool_call.id,
                }
            )

        return results

    def chat(self, message: str, history: List[Dict[str, Any]]) -> str:
        base_system = {"role": "system", "content": self._build_system_prompt()}

        context_chunks = self.rag_service.retrieve(message)

        context_message = None
        if context_chunks:
            combined_context = "\n\n".join(context_chunks)
            context_message = {
                "role": "system",
                "content": (
                    f"Here is background information about {self.name}'s career and profile. "
                    "Use it when answering the user's question:\n\n"
                    f"{combined_context}"
                ),
            }

        messages: List[Dict[str, Any]] = [base_system]
        if context_message is not None:
            messages.append(context_message)

        messages.extend(history)
        messages.append({"role": "user", "content": message})

        while True:
            try:
                response = self.openai.chat.completions.create(
                    model=settings.openai_model,
                    messages=messages,
                    tools=tools,
                )
            except Exception as e:
                logger.error(f"OpenAI chat completion failed: {e}")
                raise OpenAIError() from e

            choice = response.choices[0]

            if choice.finish_reason == "tool_calls":
                message_obj = choice.message
                tool_calls = message_obj.tool_calls
                tool_results = self._handle_tool_calls(tool_calls)
                messages.append(message_obj)
                messages.extend(tool_results)
                continue

            return response.choices[0].message.content or ""

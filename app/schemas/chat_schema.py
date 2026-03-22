from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        description="The user's message to the AI agent",
        examples=["What technologies has you worked with?"],
    )
    session_id: str | None = Field(
        default=None,
        description="Optional session ID to continue an existing conversation",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )


class ChatResponse(BaseModel):
    session_id: str = Field(description="Session ID for continuing the conversation")
    response: str = Field(description="The agent's response")

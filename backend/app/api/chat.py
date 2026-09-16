from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Optional

from app.database import get_db
from app.models.schema import ChatRequestSchema, CitationSchema, ArtifactSchema
from app.core.agent import AgentOrchestrator

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatResponseSchema(BaseModel):
    response: str
    citations: List[CitationSchema]
    artifacts: List[ArtifactSchema]

@router.post("/message", response_model=ChatResponseSchema)
async def post_chat_message(payload: ChatRequestSchema, db: AsyncSession = Depends(get_db)):
    """
    Process a user message in a chat session.
    Retrieves grounded context, calls configured LLM provider, generates citations and artifacts.
    """
    try:
        response_text, citations, artifacts = await AgentOrchestrator.process_chat(
            session_id=payload.session_id,
            user_message=payload.message,
            db=db,
            provider_name=payload.provider,
            mode=payload.mode or "chat"
        )
        return ChatResponseSchema(
            response=response_text,
            citations=citations,
            artifacts=artifacts
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process chat: {str(e)}")

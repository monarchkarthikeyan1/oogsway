from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.schema import SessionDB, MessageDB, SessionSchema, SessionCreateSchema, MessageSchema, CitationSchema, ArtifactSchema

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.get("", response_model=List[SessionSchema])
async def list_sessions(db: AsyncSession = Depends(get_db)):
    """List all active chat sessions ordered by last update time"""
    stmt = select(SessionDB).order_by(SessionDB.updated_at.desc())
    res = await db.execute(stmt)
    sessions = res.scalars().all()
    
    output = []
    for s in sessions:
        output.append(SessionSchema(
            id=s.id,
            title=s.title,
            provider=s.provider,
            created_at=s.created_at,
            updated_at=s.updated_at,
            messages=[]
        ))
    return output


@router.post("", response_model=SessionSchema, status_code=status.HTTP_201_CREATED)
async def create_session(payload: SessionCreateSchema, db: AsyncSession = Depends(get_db)):
    """Create a new independent chat session"""
    session_obj = SessionDB(
        title=payload.title or "New Growth Chat",
        provider=payload.provider or "ollama"
    )
    db.add(session_obj)
    await db.commit()
    await db.refresh(session_obj)

    return SessionSchema(
        id=session_obj.id,
        title=session_obj.title,
        provider=session_obj.provider,
        created_at=session_obj.created_at,
        updated_at=session_obj.updated_at,
        messages=[]
    )


@router.get("/{session_id}", response_model=SessionSchema)
async def get_session(session_id: str, db: AsyncSession = Depends(get_db)):
    """Get detailed chat session history with messages, citations, and artifacts"""
    stmt = select(SessionDB).options(
        selectinload(SessionDB.messages).selectinload(MessageDB.artifacts)
    ).where(SessionDB.id == session_id)
    res = await db.execute(stmt)
    s = res.scalar_one_or_none()

    if not s:
        raise HTTPException(status_code=404, detail="Session not found")

    messages_schema = []
    for m in s.messages:
        citations = [CitationSchema(**c) for c in (m.citations or [])]
        artifacts = [
            ArtifactSchema(
                id=a.id,
                session_id=a.session_id,
                message_id=a.message_id,
                title=a.title,
                artifact_type=a.artifact_type,
                content=a.content,
                language=a.language,
                created_at=a.created_at
            ) for a in m.artifacts
        ]
        messages_schema.append(MessageSchema(
            id=m.id,
            session_id=m.session_id,
            role=m.role,
            content=m.content,
            citations=citations,
            artifacts=artifacts,
            created_at=m.created_at
        ))

    return SessionSchema(
        id=s.id,
        title=s.title,
        provider=s.provider,
        created_at=s.created_at,
        updated_at=s.updated_at,
        messages=messages_schema
    )


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a chat session and all associated messages and artifacts"""
    stmt = delete(SessionDB).where(SessionDB.id == session_id)
    await db.execute(stmt)
    await db.commit()
    return None

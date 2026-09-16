from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.schema import ArtifactDB, ArtifactSchema

router = APIRouter(prefix="/artifacts", tags=["Artifacts"])

@router.get("/{artifact_id}", response_model=ArtifactSchema)
async def get_artifact(artifact_id: str, db: AsyncSession = Depends(get_db)):
    """Fetch an artifact by its ID"""
    stmt = select(ArtifactDB).where(ArtifactDB.id == artifact_id)
    res = await db.execute(stmt)
    art = res.scalar_one_or_none()
    if not art:
        raise HTTPException(status_code=404, detail="Artifact not found")

    return ArtifactSchema(
        id=art.id,
        session_id=art.session_id,
        message_id=art.message_id,
        title=art.title,
        artifact_type=art.artifact_type,
        content=art.content,
        language=art.language,
        created_at=art.created_at
    )

@router.get("/session/{session_id}", response_model=List[ArtifactSchema])
async def get_session_artifacts(session_id: str, db: AsyncSession = Depends(get_db)):
    """List all artifacts generated within a specific chat session"""
    stmt = select(ArtifactDB).where(ArtifactDB.session_id == session_id).order_by(ArtifactDB.created_at.desc())
    res = await db.execute(stmt)
    artifacts = res.scalars().all()

    return [
        ArtifactSchema(
            id=a.id,
            session_id=a.session_id,
            message_id=a.message_id,
            title=a.title,
            artifact_type=a.artifact_type,
            content=a.content,
            language=a.language,
            created_at=a.created_at
        ) for a in artifacts
    ]

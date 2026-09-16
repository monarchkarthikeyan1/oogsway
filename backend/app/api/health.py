from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db
from app.core.llm_factory import LLMFactory

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("")
async def health_check(db: AsyncSession = Depends(get_db)):
    """System health check endpoint verifying DB connection and LLM status"""
    db_status = "healthy"
    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    provider_status = await LLMFactory.get_active_provider_status()

    return {
        "status": "online" if db_status == "healthy" else "degraded",
        "database": db_status,
        "llm_providers": provider_status
    }

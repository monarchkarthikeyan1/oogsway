import pytest
import uuid
from app.models.schema import TranscriptChunkDB
from app.core.rag_engine import RAGEngine
from tests.conftest import TestingSessionLocal

@pytest.mark.asyncio
async def test_rag_retrieval():
    async with TestingSessionLocal() as db:
        # Seed test chunk
        chunk = TranscriptChunkDB(
            id=str(uuid.uuid4()),
            episode_title="Shreyas Doshi on Product Management",
            guest="Shreyas Doshi",
            topic="LNO Framework",
            content="The LNO framework classifies tasks into Leverage, Neutral, and Overhead tasks.",
            source_url="http://example.com",
            timestamp_start="02:15",
            timestamp_end="05:00",
            chunk_index=0
        )
        db.add(chunk)
        await db.commit()

        context_str, citations = await RAGEngine.retrieve_context("Tell me about Shreyas Doshi LNO framework", db, top_k=2)

        assert "Shreyas Doshi" in context_str
        assert "LNO" in context_str
        assert len(citations) >= 1
        assert citations[0].guest == "Shreyas Doshi"

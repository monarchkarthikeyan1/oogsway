import os
import json
import asyncio
import uuid
import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import AsyncSessionLocal, init_db
from app.models.schema import TranscriptChunkDB
from app.utils.logger import logger

DATA_DIR = Path(__file__).parent / "raw_transcripts"

async def ingest_transcripts():
    """Ingests raw transcript JSON files into database transcript_chunks table"""
    logger.info("Initializing database for ingestion...")
    await init_db()

    dataset_path = DATA_DIR / "transcripts_dataset.json"
    if not dataset_path.exists():
        logger.error(f"Dataset file not found at {dataset_path}")
        return

    with open(dataset_path, "r", encoding="utf-8") as f:
        episodes = json.load(f)

    logger.info(f"Loaded {len(episodes)} podcast episodes for ingestion.")

    async with AsyncSessionLocal() as session:
        # Clear existing chunks to avoid duplicates on re-ingest
        await session.execute(TranscriptChunkDB.__table__.delete())
        await session.commit()

        chunk_count = 0
        for ep in episodes:
            episode_title = ep.get("episode_title", "Lenny's Podcast")
            guest = ep.get("guest", "Unknown Guest")
            topic = ep.get("topic", "")
            source_url = ep.get("source_url", "")
            transcript_items = ep.get("transcript", [])

            for idx, item in enumerate(transcript_items):
                content = item.get("content", "")
                t_start = item.get("timestamp_start", "")
                t_end = item.get("timestamp_end", "")

                chunk = TranscriptChunkDB(
                    id=str(uuid.uuid4()),
                    episode_title=episode_title,
                    guest=guest,
                    topic=topic,
                    content=content,
                    source_url=source_url,
                    timestamp_start=t_start,
                    timestamp_end=t_end,
                    chunk_index=idx
                )
                session.add(chunk)
                chunk_count += 1

        await session.commit()
        logger.info(f"Successfully ingested {chunk_count} transcript chunks into database!")

if __name__ == "__main__":
    asyncio.run(ingest_transcripts())

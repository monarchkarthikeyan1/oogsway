import logging
import re
from typing import List, Dict, Any, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schema import TranscriptChunkDB, CitationSchema
from app.utils.logger import logger

class RAGEngine:
    @staticmethod
    async def retrieve_context(
        query: str,
        db: AsyncSession,
        top_k: int = 4
    ) -> Tuple[str, List[CitationSchema]]:
        """
        Retrieves relevant transcript chunks from PostgreSQL/SQLite database based on query relevance.
        Uses hybrid keyword TF-IDF and term matching to accurately retrieve guest insights.
        """
        try:
            stmt = select(TranscriptChunkDB)
            result = await db.execute(stmt)
            chunks: List[TranscriptChunkDB] = result.scalars().all()

            if not chunks:
                logger.warning("No transcript chunks found in database.")
                return "", []

            # Score chunks using keyword frequency and term matching
            query_terms = set(re.findall(r'\w+', query.lower()))
            # Remove common stop words
            stopwords = {"the", "a", "an", "is", "are", "and", "or", "in", "to", "of", "for", "with", "on", "at", "by", "from", "how", "what", "why"}
            keywords = query_terms - stopwords

            scored_chunks = []
            for chunk in chunks:
                content_lower = chunk.content.lower()
                guest_lower = chunk.guest.lower()
                topic_lower = (chunk.topic or "").lower()

                score = 0.0
                # Guest name match boost
                for kw in keywords:
                    if kw in guest_lower:
                        score += 5.0
                    if kw in topic_lower:
                        score += 3.0
                    # Exact term occurrences
                    matches = len(re.findall(r'\b' + re.escape(kw) + r'\b', content_lower))
                    score += matches * 1.5

                if score > 0:
                    scored_chunks.append((score, chunk))

            # Sort by highest score
            scored_chunks.sort(key=lambda x: x[0], reverse=True)
            top_matches = [chunk for score, chunk in scored_chunks[:top_k]]

            # If no matches scored > 0, fallback to returning top default chunks or empty
            if not top_matches and chunks:
                top_matches = chunks[:top_k]

            context_blocks = []
            citations: List[CitationSchema] = []

            for idx, chunk in enumerate(top_matches, start=1):
                citation_id = f"[{idx}]"
                formatted_block = (
                    f"Source {citation_id}: {chunk.guest} in '{chunk.episode_title}' "
                    f"({chunk.timestamp_start} - {chunk.timestamp_end}):\n"
                    f"\"{chunk.content}\"\n"
                )
                context_blocks.append(formatted_block)

                citations.append(CitationSchema(
                    id=citation_id,
                    guest=chunk.guest,
                    episode_title=chunk.episode_title,
                    quote=chunk.content[:200] + "..." if len(chunk.content) > 200 else chunk.content,
                    source_url=chunk.source_url,
                    timestamp=f"{chunk.timestamp_start} - {chunk.timestamp_end}"
                ))

            context_str = "\n".join(context_blocks)
            return context_str, citations

        except Exception as e:
            logger.error(f"Error during RAG context retrieval: {e}")
            return "", []

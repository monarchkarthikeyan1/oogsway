import logging
import uuid
from typing import Dict, Any, List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.schema import MessageDB, ArtifactDB, SessionDB, CitationSchema, ArtifactSchema
from app.core.llm_factory import LLMFactory, BaseLLMProvider
from app.core.rag_engine import RAGEngine
from app.core.ship30_skill import Ship30Skill, SHIP30_SYSTEM_PROMPT
from app.core.artifact_generator import ArtifactGenerator, ARTIFACT_SYSTEM_INSTRUCTION
from app.utils.logger import logger

BASE_SYSTEM_PROMPT = """You are "The Lenny Growth Assistant", an expert AI product & growth advisor trained strictly on transcripts from Lenny's Podcast and Newsletter.

CORE GUIDELINES:
1. STRICT GROUNDING: Answer product management and growth questions using the provided transcript context. Always cite your sources using inline markers like [1], [2] corresponding to the transcript quotes.
2. HONEST UNKNOWNS: If the provided transcript context does not contain enough information to answer a question, clearly state: "Based on Lenny's podcast transcripts, I don't have enough specific information to answer that question." Do NOT make up or hallucinate product advice outside the transcript context.
3. CONVERSATIONAL & ENGAGING: Maintain a helpful, sharp, and structured tone suitable for Senior PMs, VP of Product, and Growth leaders.
4. ACTIONABLE FORMATTING: Use markdown headers, bullet points, and bold emphasis to make answers easy to digest.
""" + ARTIFACT_SYSTEM_INSTRUCTION

class AgentOrchestrator:
    @staticmethod
    async def process_chat(
        session_id: str,
        user_message: str,
        db: AsyncSession,
        provider_name: Optional[str] = None,
        mode: str = "chat"
    ) -> Tuple[str, List[CitationSchema], List[ArtifactSchema]]:
        """
        Orchestrates RAG retrieval, LLM generation, artifact parsing, and database persistence.
        """
        # 1. Fetch Session
        stmt = select(SessionDB).where(SessionDB.id == session_id)
        res = await db.execute(stmt)
        session_obj = res.scalar_one_or_none()
        if not session_obj:
            raise ValueError(f"Session {session_id} not found.")

        # Determine LLM Provider
        chosen_provider = provider_name or session_obj.provider or "ollama"
        llm = LLMFactory.get_provider(chosen_provider)

        # Ensure provider availability or fallback
        if not await llm.is_available():
            logger.warning(f"Provider {chosen_provider} unavailable. Attempting fallback to Ollama...")
            llm = LLMFactory.get_provider("ollama")
            if not await llm.is_available():
                fallback_msg = (
                    f"⚠️ The selected provider '{chosen_provider}' and local Ollama are currently unreachable.\n\n"
                    f"**Setup Instructions**:\n"
                    f"- To run locally, ensure Ollama is running (`ollama serve`) with model `llama3.2` or `mistral`.\n"
                    f"- Or supply an `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` in your `.env` file or UI Settings."
                )
                return fallback_msg, [], []

        # 2. Persist User Message
        user_msg_db = MessageDB(
            id=str(uuid.uuid4()),
            session_id=session_id,
            role="user",
            content=user_message,
            citations=[]
        )
        db.add(user_msg_db)
        await db.commit()

        # 3. Retrieve Context from Knowledge Base
        context_str, citations = await RAGEngine.retrieve_context(user_message, db, top_k=4)

        # 4. Fetch Multi-turn Conversation History
        history_stmt = select(MessageDB).where(MessageDB.session_id == session_id).order_by(MessageDB.created_at.asc())
        hist_res = await db.execute(history_stmt)
        past_messages = hist_res.scalars().all()

        formatted_history = []
        for msg in past_messages[-6:]: # Keep recent 6 turns for window context
            formatted_history.append({"role": msg.role, "content": msg.content})

        # 5. Handle Special Mode (Ship 30 Skill vs Chat vs Artifact)
        if mode == "ship30" or "ship 30" in user_message.lower() or "essay" in user_message.lower():
            logger.info("Executing Ship 30 for 30 Content Skill...")
            response_text = await Ship30Skill.generate_essay(user_message, context_str, llm)
        else:
            # Build System Prompt with Grounding Context
            system_prompt = f"{BASE_SYSTEM_PROMPT}\n\nTRANSCRIPT GROUNDING KNOWLEDGE BASE:\n{context_str}"
            response_text = await llm.generate(formatted_history, system_prompt=system_prompt)

        # 6. Parse and Save Artifacts if present
        parsed_artifacts = ArtifactGenerator.parse_artifacts_from_response(response_text)
        created_artifacts: List[ArtifactSchema] = []

        assistant_msg_id = str(uuid.uuid4())

        for art_data in parsed_artifacts:
            art_id = str(uuid.uuid4())
            rendered_content = ArtifactGenerator.prepare_rendered_artifact(
                art_data["artifact_type"],
                art_data["content"],
                art_data["title"]
            )

            art_db = ArtifactDB(
                id=art_id,
                session_id=session_id,
                message_id=assistant_msg_id,
                title=art_data["title"],
                artifact_type=art_data["artifact_type"],
                content=rendered_content,
                language="html" if art_data["artifact_type"] == "html" else "markdown"
            )
            db.add(art_db)
            created_artifacts.append(ArtifactSchema(
                id=art_db.id,
                session_id=session_id,
                message_id=assistant_msg_id,
                title=art_db.title,
                artifact_type=art_db.artifact_type,
                content=art_db.content,
                language=art_db.language,
                created_at=art_db.created_at
            ))

        # 7. Persist Assistant Message
        citations_dict = [c.model_dump() for c in citations]
        assistant_msg_db = MessageDB(
            id=assistant_msg_id,
            session_id=session_id,
            role="assistant",
            content=response_text,
            citations=citations_dict
        )
        db.add(assistant_msg_db)
        await db.commit()

        return response_text, citations, created_artifacts

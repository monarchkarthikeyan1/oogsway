import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.orm import declarative_base, relationship
from pydantic import BaseModel, Field

Base = declarative_base()

# Database ORM Models
class SessionDB(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False, default="New Growth Chat")
    provider = Column(String, nullable=False, default="ollama")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    session_metadata = Column(JSON, nullable=True, default={})

    messages = relationship("MessageDB", back_populates="session", cascade="all, delete-orphan")
    artifacts = relationship("ArtifactDB", back_populates="session", cascade="all, delete-orphan")


class MessageDB(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    role = Column(String, nullable=False) # user | assistant | system
    content = Column(Text, nullable=False)
    citations = Column(JSON, nullable=True, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("SessionDB", back_populates="messages")
    artifacts = relationship("ArtifactDB", back_populates="message")


class ArtifactDB(Base):
    __tablename__ = "artifacts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    message_id = Column(String, ForeignKey("messages.id"), nullable=True)
    title = Column(String, nullable=False)
    artifact_type = Column(String, nullable=False) # html | markdown | code | css
    content = Column(Text, nullable=False)
    language = Column(String, nullable=True, default="markdown")
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("SessionDB", back_populates="artifacts")
    message = relationship("MessageDB", back_populates="artifacts")


class TranscriptChunkDB(Base):
    __tablename__ = "transcript_chunks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    episode_title = Column(String, nullable=False)
    guest = Column(String, nullable=False)
    topic = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    source_url = Column(String, nullable=True)
    timestamp_start = Column(String, nullable=True)
    timestamp_end = Column(String, nullable=True)
    chunk_index = Column(Integer, nullable=False, default=0)


# Pydantic API Schemas

class CitationSchema(BaseModel):
    id: str
    guest: str
    episode_title: str
    quote: str
    source_url: Optional[str] = None
    timestamp: Optional[str] = None

class ArtifactSchema(BaseModel):
    id: str
    session_id: str
    message_id: Optional[str] = None
    title: str
    artifact_type: str # html | markdown | code
    content: str
    language: Optional[str] = "markdown"
    created_at: datetime

class MessageSchema(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    citations: Optional[List[CitationSchema]] = []
    artifacts: Optional[List[ArtifactSchema]] = []
    created_at: datetime

class SessionSchema(BaseModel):
    id: str
    title: str
    provider: str
    created_at: datetime
    updated_at: datetime
    messages: Optional[List[MessageSchema]] = []

class SessionCreateSchema(BaseModel):
    title: Optional[str] = "New Growth Chat"
    provider: Optional[str] = "ollama"

class ChatRequestSchema(BaseModel):
    session_id: str
    message: str
    provider: Optional[str] = None # Optional override (ollama | anthropic | openai)
    mode: Optional[str] = "chat" # chat | ship30 | artifact

class ProviderStatusSchema(BaseModel):
    current_provider: str
    ollama_available: bool
    ollama_model: str
    anthropic_available: bool
    openai_available: bool
    active_models: Dict[str, str]

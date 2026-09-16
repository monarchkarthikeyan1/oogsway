from fastapi import APIRouter
from pydantic import BaseModel
from app.config import settings
from app.core.llm_factory import LLMFactory
from app.models.schema import ProviderStatusSchema

router = APIRouter(prefix="/providers", tags=["Providers"])

class ToggleProviderPayload(BaseModel):
    provider: str # ollama | anthropic | openai

@router.get("", response_model=ProviderStatusSchema)
async def get_providers_status():
    """Get active status and configuration of all LLM providers (Ollama, Anthropic, OpenAI)"""
    return await LLMFactory.get_active_provider_status()

@router.post("/toggle", response_model=ProviderStatusSchema)
async def toggle_provider(payload: ToggleProviderPayload):
    """Dynamically switch the default LLM provider for the application"""
    provider_name = payload.provider.lower().strip()
    if provider_name in ["ollama", "anthropic", "openai"]:
        settings.DEFAULT_PROVIDER = provider_name
    
    return await LLMFactory.get_active_provider_status()

import json
import logging
from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, List, Any, Optional
import httpx
from app.config import settings

logger = logging.getLogger("lenny_assistant.llm_factory")

class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate(self, messages: List[Dict[str, str]], system_prompt: Optional[str] = None) -> str:
        pass

    @abstractmethod
    async def is_available(self) -> bool:
        pass

class OllamaProvider(BaseLLMProvider):
    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip('/')
        self.model = model or settings.OLLAMA_MODEL

    async def is_available(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.get(f"{self.base_url}/api/tags")
                return res.status_code == 200
        except Exception as e:
            logger.debug(f"Ollama health check failed: {e}")
            return False

    async def generate(self, messages: List[Dict[str, str]], system_prompt: Optional[str] = None) -> str:
        formatted_messages = []
        if system_prompt:
            formatted_messages.append({"role": "system", "content": system_prompt})
        formatted_messages.extend(messages)

        payload = {
            "model": self.model,
            "messages": formatted_messages,
            "stream": False,
            "options": {"temperature": 0.3}
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                res = await client.post(f"{self.base_url}/api/chat", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    return data.get("message", {}).get("content", "")
                else:
                    raise RuntimeError(f"Ollama returned HTTP {res.status_code}: {res.text}")
        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            raise e


class AnthropicProvider(BaseLLMProvider):
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self.model = model or settings.ANTHROPIC_MODEL

    async def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 5)

    async def generate(self, messages: List[Dict[str, str]], system_prompt: Optional[str] = None) -> str:
        if not await self.is_available():
            raise ValueError("Anthropic API key is not configured in environment or settings.")

        try:
            from anthropic import AsyncAnthropic
            client = AsyncAnthropic(api_key=self.api_key)

            # Convert system message if inside messages list
            anthropic_messages = []
            sys_content = system_prompt or ""

            for msg in messages:
                if msg["role"] == "system":
                    sys_content += ("\n" + msg["content"])
                else:
                    anthropic_messages.append({"role": msg["role"], "content": msg["content"]})

            response = await client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=sys_content if sys_content else None,
                messages=anthropic_messages
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic generation error: {e}")
            raise e


class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.OPENAI_MODEL

    async def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 5)

    async def generate(self, messages: List[Dict[str, str]], system_prompt: Optional[str] = None) -> str:
        if not await self.is_available():
            raise ValueError("OpenAI API key is not configured in environment or settings.")

        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=self.api_key)

            formatted_messages = []
            if system_prompt:
                formatted_messages.append({"role": "system", "content": system_prompt})
            formatted_messages.extend(messages)

            response = await client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=0.3
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"OpenAI generation error: {e}")
            raise e


class LLMFactory:
    @staticmethod
    def get_provider(provider_name: str = "ollama") -> BaseLLMProvider:
        provider_name = provider_name.lower().strip()
        if provider_name == "anthropic":
            return AnthropicProvider()
        elif provider_name == "openai":
            return OpenAIProvider()
        else:
            return OllamaProvider()

    @staticmethod
    async def get_active_provider_status() -> Dict[str, Any]:
        ollama = OllamaProvider()
        anthropic = AnthropicProvider()
        openai = OpenAIProvider()

        ollama_ok = await ollama.is_available()
        anthropic_ok = await anthropic.is_available()
        openai_ok = await openai.is_available()

        return {
            "current_provider": settings.DEFAULT_PROVIDER,
            "ollama_available": ollama_ok,
            "ollama_model": settings.OLLAMA_MODEL,
            "anthropic_available": anthropic_ok,
            "openai_available": openai_ok,
            "active_models": {
                "ollama": settings.OLLAMA_MODEL,
                "anthropic": settings.ANTHROPIC_MODEL,
                "openai": settings.OPENAI_MODEL
            }
        }

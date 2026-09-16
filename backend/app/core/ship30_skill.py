import logging
from typing import Dict, Any, List
from app.core.llm_factory import BaseLLMProvider
from app.models.schema import CitationSchema

logger = logging.getLogger("lenny_assistant.ship30_skill")

SHIP30_SYSTEM_PROMPT = """You are an elite Ship 30 for 30 Growth Writer and Product Strategist.
Your task is to transform raw product management & growth insights into an authoritative, publication-ready Ship 30 for 30 style essay.

STRICT WRITING & STRUCTURAL PRINCIPLES:
1. WORD COUNT: The essay MUST be approximately 1,250 words long. Detailed, thorough, and punchy.
2. THE HOOK: Start with an attention-grabbing Headline, Subhead, and a 2-sentence opening hook that challenges conventional wisdom.
3. NARRATIVE PROGRESSION:
   - Part 1: The Problem & Status Quo (Why traditional thinking fails)
   - Part 2: The Mindset Shift (The counter-intuitive insight from Lenny's Podcast guest)
   - Part 3: The 4-Step Tactical Execution Framework (Detailed, step-by-step implementation)
   - Part 4: The 3 Pitfalls to Avoid
   - Part 5: The Specific, Actionable Takeaway Checklist
4. SKIMMABLE FORMATTING:
   - Short paragraphs (1-3 sentences maximum).
   - Frequent H2 and H3 subheadings.
   - Selective BOLD lead-ins for every bullet point (e.g. "**Step 1: Audit your energy distribution** — ...").
   - Callout blocks (`> [!NOTE]`) for key quotes.
5. GROUNDED CITATIONS:
   - Ground every core claim in the provided Lenny's Podcast transcript sources.
   - Reference the guest explicitly (e.g., "As Shreyas Doshi explained...", "According to Elena Verna...").
   - Include inline source markers like [1], [2] matching the provided context.

Do not write meta-commentary or conversational intros. Return ONLY the fully formatted Markdown essay.
"""

class Ship30Skill:
    @staticmethod
    async def generate_essay(
        topic_or_query: str,
        context_str: str,
        llm_provider: BaseLLMProvider
    ) -> str:
        """
        Executes the Ship 30 for 30 content generation skill.
        Encodes structural rules to produce a 1,250-word grounded essay.
        """
        user_prompt = f"""Generate a comprehensive ~1,250 word Ship 30 for 30 essay on the following topic:

Topic: {topic_or_query}

Grounding Context from Lenny's Podcast Transcripts:
{context_str}

Remember to follow all Ship 30 formatting rules: ~1,250 words, bold lead-in bullets, short paragraphs, strong hook, tactical frameworks, and transcript citations."""

        messages = [{"role": "user", "content": user_prompt}]

        try:
            essay = await llm_provider.generate(messages, system_prompt=SHIP30_SYSTEM_PROMPT)
            return essay
        except Exception as e:
            logger.error(f"Error generating Ship 30 essay: {e}")
            raise e

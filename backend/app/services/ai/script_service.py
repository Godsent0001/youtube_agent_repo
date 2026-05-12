import json
import re

from app.services.ai.llm_client import llm_client
from app.core.logger import logger


class ScriptService:
    """
    LLM-powered script generator for viral YouTube content
    """

    def __init__(self):
        self.logger = logger

    # =========================
    # MAIN GENERATION
    # =========================
    def generate_script(self, topic: str, niche: str, content_type: str, research: dict):

        messages = [
            {
                "role": "system",
                "content": """
You are a world-class YouTube script writer specializing in viral content.

CRITICAL RULES (VERY IMPORTANT):
- NEVER use numbering (1, 2, 3, 01, 002, etc.)
- NEVER format as a list
- NEVER write "Scene 1", "Step 1", etc.
- Write ONLY natural spoken narration
- Script must sound like a human talking, not a document
- Avoid meta commentary (no "in this video", no instructions)
- AT THE END of the script, include a short, natural call to action (like and subscribe) that fits the flow.

YOUR JOB:
- Write highly engaging scripts optimized for watch time
- Use storytelling, hooks, tension, payoff
- Make it emotionally engaging and natural
- Keep pacing fast and addictive
- Ensure the "like and subscribe" CTA feels part of the narrative, not forced.

OUTPUT FORMAT (ONLY VALID JSON):

{
  "script": "natural spoken narration only (including the natural CTA at the end)",
  "hook": "strong opening line",
  "key_moments": ["moment 1", "moment 2", "moment 3"],
  "cta": "short call to action (repeated here for reference)"
}
"""
            },
            {
                "role": "user",
                "content": f"""
Topic: {topic}
Niche: {niche}
Content Type: {content_type}

Research Data:
{json.dumps(research, indent=2)}
"""
            }
        ]

        response = llm_client.generate(messages)

        try:
            cleaned = self._clean_response(response)
            parsed = json.loads(cleaned)

            return {
                "script": self._clean_script(parsed.get("script", "")),
                "hook": parsed.get("hook", ""),
                "key_moments": parsed.get("key_moments", []),
                "cta": parsed.get("cta", "")
            }

        except Exception as e:
            self.logger.error(f"Script generation failed: {e}")

            return {
                "script": "",
                "hook": "",
                "key_moments": [],
                "cta": ""
            }

    # =========================
    # CLEAN LLM OUTPUT
    # =========================
    def _clean_response(self, text: str) -> str:
        """
        Fix common LLM JSON breaking issues
        """

        if not text:
            return "{}"

        # remove markdown code blocks
        text = text.replace("```json", "").replace("```", "")

        # sometimes models add commentary before JSON
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return match.group(0)

        return text.strip()

    # =========================
    # REMOVE NUMBERING FROM SCRIPT
    # =========================
    def _clean_script(self, script: str) -> str:
        """
        Removes hidden numbering that causes ElevenLabs to read "003", "004"
        """

        if not script:
            return ""

        # remove numbered bullets (1. 2. 3.)
        script = re.sub(r"\b\d+\.\s*", "", script)

        # remove weird zero-padded numbers (001, 002, 003)
        script = re.sub(r"\b0+\d+\b", "", script)

        # remove step labels
        script = re.sub(r"\b(step|scene)\s*\d+\b", "", script, flags=re.IGNORECASE)

        # normalize spaces
        script = re.sub(r"\s+", " ", script).strip()

        return script


# Singleton
script_service = ScriptService()
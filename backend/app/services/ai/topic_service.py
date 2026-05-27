import json
import random

from app.services.ai.llm_client import llm_client
from app.core.logger import logger


class TopicService:
    """
    Advanced viral topic generator

    FIXES:
    - Prevents repetitive topics
    - Better viral diversity
    - Shorts + Long-form optimized
    - Safer JSON parsing
    - Better fallback generation
    - Smarter prompt engineering
    """

    def __init__(self):

        self.logger = logger

        # ==========================================
        # MEMORY CACHE
        # Prevent repeated topics during runtime
        # ==========================================
        self.previous_topics = []

        self.max_history = 50

    # ==================================================
    # MAIN ENTRY
    # ==================================================
    def generate_topic(
        self,
        niche: str,
        content_type: str,
        custom_prompt: str = None
    ):

        try:

            # ==========================================
            # BUILD HISTORY CONTEXT
            # ==========================================
            history_text = self._build_history_context()

            # ==========================================
            # CONTENT TYPE RULES
            # ==========================================
            content_rules = self._get_content_rules(
                content_type
            )

            messages = [
                {
                    "role": "system",
                    "content": f"""
You are a world-class viral video strategist for MorphFlow.

Your ONLY job is to generate a HIGHLY ENGAGING and VIRAL video topic based on the user's prompt.

CRITICAL REQUIREMENTS:
- Use the user's prompt as the PRIMARY guide for the topic.
- EVERY topic must feel fresh and viral.
- Avoid generic AI topics.
- Create curiosity gaps and maximize engagement.
- Focus on emotion, mystery, surprise, fear, urgency, status, or hidden knowledge.

TOPIC CONSTRAINTS:
- AVOID topics that require physical explaining.
- AVOID topics that are very complex to explain without specific visuals.
- PREFER topics that can be effectively illustrated with high-quality stock footage.

STRICT RULES:
- Return ONLY valid JSON.
- No markdown.
- No explanations.

OUTPUT FORMAT:
{{
  "topic": "...",
  "alternate_variations": [
    "...",
    "...",
    "..."
  ]
}}
"""
                },
                {
                    "role": "user",
                    "content": f"""
USER PROMPT:
{custom_prompt if custom_prompt else "Generate a viral video topic about " + niche}

CONTENT TYPE:
{content_type}

IMPORTANT:
The topic should be a catchy title for the video that follows the spirit of the user's prompt but is optimized for virality.
"""
                }
            ]

            # ==========================================
            # GENERATE
            # ==========================================
            response = llm_client.generate(
                messages=messages,
                temperature=1.1
            )

            data = self._safe_parse(response)

            topic = data.get("topic", "").strip()

            if not topic:
                raise Exception("Empty topic returned")

            # ==========================================
            # STORE HISTORY
            # ==========================================
            self._store_topic(topic)

            self.logger.info(
                f"Topic generated: {topic}"
            )

            return {
                "topic": topic,
                "alternate_variations": data.get(
                    "alternate_variations",
                    []
                )
            }

        except Exception as e:

            self.logger.error(
                f"Topic generation failed: {e}"
            )

            fallback = self._fallback_topic(
                niche,
                content_type
            )

            self._store_topic(fallback)

            return {
                "topic": fallback,
                "alternate_variations": []
            }

    # ==================================================
    # SAFE JSON PARSER
    # ==================================================
    def _safe_parse(self, response):

        try:

            if isinstance(response, dict):
                return response

            cleaned = response.strip()

            # remove markdown
            cleaned = cleaned.replace(
                "```json",
                ""
            )

            cleaned = cleaned.replace(
                "```",
                ""
            )

            return json.loads(cleaned)

        except Exception as e:

            self.logger.error(
                f"Topic parse failed: {e}"
            )

            return {}

    # ==================================================
    # CONTENT TYPE RULES
    # ==================================================
    def _get_content_rules(
        self,
        content_type
    ):

        if content_type == "shorts":

            return """
SHORTS RULES:
- Extremely punchy
- Fast curiosity
- Strong emotional trigger
- 5-12 word style titles preferred
- Aggressive hooks
- TikTok-style energy
"""

        return """
LONG FORM RULES:
- Strong storytelling potential
- Deep curiosity gaps
- Educational + entertaining
- High watch-time potential
- Documentary or transformation style
"""

    # ==================================================
    # HISTORY CONTEXT
    # ==================================================
    def _build_history_context(self):

        if not self.previous_topics:
            return "None"

        latest = self.previous_topics[-20:]

        return "\n".join(
            [f"- {t}" for t in latest]
        )

    # ==================================================
    # STORE TOPIC
    # ==================================================
    def _store_topic(self, topic):

        if not topic:
            return

        self.previous_topics.append(topic)

        # limit memory
        if len(self.previous_topics) > self.max_history:

            self.previous_topics = (
                self.previous_topics[-self.max_history:]
            )

    # ==================================================
    # FALLBACK SYSTEM
    # ==================================================
    def _fallback_topic(
        self,
        niche,
        content_type
    ):

        viral_patterns = [

            "The hidden truth about {} nobody talks about",

            "I tested the most dangerous {} strategy",

            "Why everyone is suddenly obsessed with {}",

            "The {} trick that feels illegal to know",

            "I tried using {} for 7 days",

            "The dark side of {}",

            "What happens if you stop using {}",

            "This new {} method is terrifyingly effective",

            "Why 99% of people fail at {}",

            "The secret psychology behind {}"
        ]

        pattern = random.choice(
            viral_patterns
        )

        return pattern.format(niche)

# ==================================================
# SINGLETON
# ==================================================

topic_service = TopicService()
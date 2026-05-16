import json
import re
from typing import List, Dict, Any

from app.core.logger import logger
from app.services.ai.llm_client import llm_client


class SceneService:
    """
    Converts scripts into cinematic AI video scenes.

    OPTIMIZED FOR:
    - Better Pixabay matching
    - Better narration pacing
    - Better scene diversity
    - Cleaner stock queries
    - Faster rendering pipeline
    - Video-first AI Shorts generation
    """

    def __init__(self):

        self.logger = logger

    # =====================================
    # MAIN ENTRY
    # =====================================

    def generate_scenes(
        self,
        script: str,
        content_type: str,
        video_length: int = None
    ) -> List[Dict[str, Any]]:

        is_shorts = (
            content_type.lower() == "shorts"
        )

        rules = self._get_scene_rules(
            is_shorts,
            video_length
        )

        messages = [
            {
                "role": "system",
                "content": f"""
You are a world-class viral YouTube Shorts director.

Your task:
Convert scripts into cinematic scenes for AI-generated videos.

RETURN JSON ONLY.

==================================================
VERY IMPORTANT PIPELINE RULES
==================================================

Each scene MUST contain:

1. text
- natural narration
- conversational
- emotionally engaging
- SHORT sentences preferred

2. visual_query
- cinematic description
- emotionally visual
- descriptive
- for internal AI understanding

3. stock_query
- VERY SIMPLE Pixabay-safe keywords
- ONLY 2 to 5 words
- must work well for stock videos/images

4. emotion
- emotional tone

5. media_type_preference
- "video" or "image"

6. duration_seconds

==================================================
CRITICAL STOCK QUERY RULES
==================================================

stock_query MUST be:
- short
- simple
- visual
- searchable on Pixabay

GOOD:
- hacker typing laptop
- shocked woman phone
- city traffic night
- robot face
- stock market screen
- burning money
- crying child

BAD:
- cinematic futuristic hacker using glowing AI hologram interface in dark neon room

NEVER:
- use full sentences
- use abstract concepts
- use poetic language
- use AI buzzwords excessively

==================================================
VIDEO-FIRST RULE
==================================================

Scenes with:
- movement
- tension
- fear
- action
- shock
- excitement
- dramatic emotion

SHOULD use:
media_type_preference = "video"

Calmer scenes:
media_type_preference = "image"

==================================================
PACING RULES
==================================================

- narration must fit naturally
- avoid overly long narration per scene
- each scene should feel visually distinct
- avoid repeating same visual idea

==================================================
OUTPUT FORMAT
==================================================

{{
  "scenes": [
    {{
      "text": "spoken narration",
      "visual_query": "cinematic visual description",
      "stock_query": "simple stock keywords",
      "emotion": "shock",
      "media_type_preference": "video",
      "duration_seconds": 4
    }}
  ]
}}

{rules}
"""
            },
            {
                "role": "user",
                "content": f"""
CONTENT TYPE:
{content_type}

SCRIPT:
{script}
"""
            }
        ]

        try:

            response = llm_client.generate(
                messages,
                temperature=0.85
            )

            scenes_data = self._safe_parse(
                response
            )

            scenes = scenes_data.get(
                "scenes",
                []
            )

            validated = self._validate_scenes(
                scenes,
                is_shorts
            )

            self.logger.info(
                f"Generated {len(validated)} scenes"
            )

            return validated

        except Exception as e:

            self.logger.error(
                f"Scene generation failed: {e}"
            )

            return self._fallback_scenes(
                script,
                is_shorts
            )

    # =====================================
    # RULES
    # =====================================

    def _get_scene_rules(
        self,
        is_shorts: bool,
        video_length: int = None
    ):

        if is_shorts:
            num_scenes = "7 to 12"
            if video_length and video_length < 30:
                num_scenes = "4 to 6"

            return f"""
SHORTS RULES:
- Create {num_scenes} scenes
- Fast pacing
- Strong emotional movement
- Strong hook in first scene
- Keep narration concise
- Use visually dynamic moments
- Average 3 to 5 seconds per scene
"""

        num_scenes = "10 to 25"
        if video_length:
            # simple heuristic: ~3-4 scenes per minute
            if video_length < 20: # minutes
                num_scenes = f"{max(10, video_length * 3)} to {max(15, video_length * 5)}"
            else: # seconds
                num_scenes = f"{max(5, video_length // 10)} to {max(8, video_length // 6)}"

        return f"""
LONG FORM RULES:
- Create {num_scenes} scenes
- Slower cinematic pacing
- Build narrative progression
- Mix calm and intense scenes
- Average 5 to 8 seconds per scene
"""

    # =====================================
    # SAFE PARSER
    # =====================================

    def _safe_parse(
        self,
        response: str
    ) -> dict:

        try:

            if isinstance(response, dict):
                return response

            cleaned = response.strip()

            cleaned = re.sub(
                r"```json",
                "",
                cleaned
            )

            cleaned = re.sub(
                r"```",
                "",
                cleaned
            )

            cleaned = cleaned.strip()

            return json.loads(cleaned)

        except Exception as e:

            self.logger.error(
                f"Scene JSON parse error: {e}"
            )

            return {"scenes": []}

    # =====================================
    # VALIDATION
    # =====================================

    def _validate_scenes(
        self,
        scenes: List[dict],
        is_shorts: bool
    ) -> List[dict]:

        validated = []

        used_stock_queries = set()

        for scene in scenes:

            try:

                if not isinstance(scene, dict):
                    continue

                text = self._clean_text(
                    scene.get("text", "")
                )

                visual_query = self._clean_text(
                    scene.get(
                        "visual_query",
                        ""
                    )
                )

                stock_query = self._clean_stock_query(
                    scene.get(
                        "stock_query",
                        text
                    )
                )

                emotion = (
                    scene.get(
                        "emotion",
                        "neutral"
                    )
                    .strip()
                    .lower()
                )

                media_pref = (
                    scene.get(
                        "media_type_preference",
                        "image"
                    )
                    .strip()
                    .lower()
                )

                duration = scene.get(
                    "duration_seconds",
                    4 if is_shorts else 6
                )

                # ==================================
                # REQUIRED TEXT
                # ==================================

                if not text:
                    continue

                # ==================================
                # PREVENT DUPLICATE QUERIES
                # ==================================

                if stock_query in used_stock_queries:

                    stock_query += " cinematic"

                used_stock_queries.add(
                    stock_query
                )

                # ==================================
                # SAFETY
                # ==================================

                if media_pref not in [
                    "video",
                    "image"
                ]:
                    media_pref = "image"

                # ==================================
                # AUTO VIDEO PRIORITY
                # ==================================

                if emotion in [
                    "shock",
                    "fear",
                    "action",
                    "tension",
                    "excitement",
                    "dramatic"
                ]:
                    media_pref = "video"

                validated.append({
                    "text": text,

                    "visual_query": (
                        visual_query or stock_query
                    ),

                    "stock_query": stock_query,

                    "emotion": emotion,

                    "media_type_preference": media_pref,

                    "duration_seconds":
                        self._clamp_duration(
                            duration,
                            is_shorts
                        )
                })

            except Exception:
                continue

        return validated

    # =====================================
    # TEXT CLEANER
    # =====================================

    def _clean_text(
        self,
        text: str
    ):

        text = re.sub(
            r"^\d+[\.\)\-\s]*",
            "",
            text
        )

        text = re.sub(
            r"scene\s*\d+",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # =====================================
    # STOCK QUERY CLEANER
    # =====================================

    def _clean_stock_query(
        self,
        query: str
    ):

        query = query.strip().lower()

        query = re.sub(
            r"[^a-z0-9\s]",
            "",
            query
        )

        query = re.sub(
            r"\s+",
            " ",
            query
        )

        # ==================================
        # IMPORTANT:
        # keep stock queries short
        # ==================================

        words = query.split()[:5]

        query = " ".join(words)

        if not query:
            query = "technology"

        return query[:60]

    # =====================================
    # DURATION CONTROL
    # =====================================

    def _clamp_duration(
        self,
        duration,
        is_shorts: bool
    ):

        try:

            duration = float(duration)

        except:

            duration = (
                4 if is_shorts else 6
            )

        if is_shorts:

            return max(
                3,
                min(duration, 6)
            )

        return max(
            4,
            min(duration, 12)
        )

    # =====================================
    # FALLBACK SCENES
    # =====================================

    def _fallback_scenes(
        self,
        script: str,
        is_shorts: bool
    ):

        sentences = re.split(
            r'(?<=[.!?])\s+',
            script
        )

        scenes = []

        max_scenes = (
            10 if is_shorts else 15
        )

        for sentence in sentences[:max_scenes]:

            clean = self._clean_text(
                sentence
            )

            if not clean:
                continue

            stock_query = self._clean_stock_query(
                clean
            )

            scenes.append({

                "text": clean,

                "visual_query": clean,

                "stock_query": stock_query,

                "emotion": "neutral",

                "media_type_preference": "image",

                "duration_seconds":
                    4 if is_shorts else 6
            })

        return scenes


# =====================================
# SINGLETON
# =====================================

scene_service = SceneService()
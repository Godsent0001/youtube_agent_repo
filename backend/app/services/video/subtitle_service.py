import re
from app.core.logger import logger


class SubtitleService:
    """
    Generates timed subtitles for video scenes
    """

    def __init__(self):
        self.logger = logger

    def generate_subtitles(self, script: str, total_duration: int):

        if not script or not script.strip():
            self.logger.warning("Empty script received")
            return []

        script = self._clean_script(script)
        sentences = self._split_script(script)

        if not sentences:
            return []

        avg_duration = max(total_duration // len(sentences), 1)

        subtitles = []
        current_time = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            subtitles.append({
                "text": sentence,
                "start": current_time,
                "end": current_time + avg_duration
            })

            current_time += avg_duration

        self.logger.info(f"Generated {len(subtitles)} subtitles")
        return subtitles

    def _clean_script(self, script: str):
        script = script.replace("\n", " ")
        script = re.sub(r'\b\d{1,4}[\.\)]?\s*', '', script)
        script = re.sub(r'\s+', ' ', script)
        return script.strip()

    def _split_script(self, script: str):
        sentences = re.split(r'(?<=[.!?])\s+', script)
        return [s.strip() for s in sentences if len(s.strip()) > 2]


# ✅ THIS IS WHAT YOU WERE MISSING
subtitle_service = SubtitleService()
from app.core.logger import logger


class SubtitleService:
    """
    Generates subtitles for video based on script
    (MVP: script-based timing approximation)
    """

    def __init__(self):
        self.logger = logger

    def generate_subtitles(self, script: str, total_duration: int):

        """
        Converts script → timed subtitle chunks
        """

        sentences = self._split_script(script)

        if not sentences:
            return []

        avg_duration = max(total_duration // len(sentences), 1)

        subtitles = []

        current_time = 0

        for sentence in sentences:

            subtitles.append({
                "text": sentence,
                "start": current_time,
                "end": current_time + avg_duration
            })

            current_time += avg_duration

        self.logger.info(f"Generated {len(subtitles)} subtitles")

        return subtitles

    def _split_script(self, script: str):

        """
        Smart sentence splitting (simple but safe)
        """

        script = script.replace("\n", " ")
        sentences = script.split(".")

        return [s.strip() for s in sentences if s.strip()]
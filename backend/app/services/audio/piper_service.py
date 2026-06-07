import os
import subprocess
import uuid
import sys
from app.core.logger import logger

class PiperService:
    """
    Local Piper TTS service
    """

    def __init__(self):
        self.logger = logger
        self.model_path = "/app/models/en_US-lessac-medium.onnx"
        self.output_dir = "storage/audio"

    def generate_audio(self, text: str):
        """
        Generates audio from text using Piper.
        """
        os.makedirs(self.output_dir, exist_ok=True)
        file_path = os.path.join(self.output_dir, f"{uuid.uuid4()}.wav")

        try:
            self.logger.info(f"Generating Piper TTS for: {text[:50]}...")

            # Attempt to use the piper-tts python library
            try:
                from piper.voice import PiperVoice

                if not os.path.exists(self.model_path):
                    self.logger.warning(f"Piper model not found at {self.model_path}. Falling back to mock.")
                    return self._mock_audio(file_path)

                voice = PiperVoice.load(self.model_path)
                with open(file_path, "wb") as wav_file:
                    voice.synthesize(text, wav_file)

                self.logger.info(f"Piper audio generated: {file_path}")
                return file_path

            except ImportError:
                self.logger.warning("piper-voice python module not found. Trying CLI fallback.")
                return self._run_cli(text, file_path)
            except Exception as e:
                self.logger.error(f"Piper python library failed: {e}")
                return self._run_cli(text, file_path)

        except Exception as e:
            self.logger.error(f"Piper TTS total failure: {e}")
            return self._mock_audio(file_path)

    def _run_cli(self, text: str, file_path: str):
        """
        Safe CLI execution for Piper.
        """
        try:
            self.logger.info("Running Piper CLI...")
            # Use subprocess.run with a list for safety against shell injection
            process = subprocess.Popen(
                ["piper", "--model", self.model_path, "--output_file", file_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(input=text)

            if process.returncode == 0:
                self.logger.info(f"Piper CLI success: {file_path}")
                return file_path
            else:
                self.logger.error(f"Piper CLI error: {stderr}")
                return self._mock_audio(file_path)
        except Exception as e:
            self.logger.error(f"Piper CLI execution failed: {e}")
            return self._mock_audio(file_path)

    def _mock_audio(self, file_path):
        with open(file_path, "wb") as f:
            f.write(b"MOCK PIPER AUDIO CONTENT")
        self.logger.info(f"MOCK Piper audio generated: {file_path}")
        return file_path

# singleton
piper_service = PiperService()

import os
import subprocess
import uuid
from app.core.logger import logger


class PiperService:
    """
    Local Piper TTS service
    """

    def __init__(self):
        self.logger = logger

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(__file__)
            )
        )

        docker_path = "/app/models/en_US-lessac-medium.onnx"

        local_path = os.path.join(
            base_dir,
            "models/en_US-lessac-medium.onnx"
        )

        if os.path.exists(docker_path):
            self.model_path = docker_path

        else:
            self.model_path = local_path


        self.output_dir = "storage/audio"

        os.makedirs(
            self.output_dir,
            exist_ok=True
        )

        self.logger.info(
            f"Piper model: {self.model_path}"
        )


    def generate_audio(self, text: str):

        file_path = os.path.join(
            self.output_dir,
            f"{uuid.uuid4()}.wav"
        )


        try:

            self.logger.info(
                f"Generating Piper TTS for: {text[:50]}..."
            )


            # Try python Piper first
            try:

                from piper.voice import PiperVoice


                if os.path.exists(self.model_path):

                    voice = PiperVoice.load(
                        self.model_path
                    )


                    with open(
                        file_path,
                        "wb"
                    ) as wav_file:

                        voice.synthesize(
                            text,
                            wav_file
                        )


                    size = os.path.getsize(
                        file_path
                    )


                    if size > 0:

                        self.logger.info(
                            f"Piper python success: {file_path} ({size} bytes)"
                        )

                        return file_path


                    else:

                        self.logger.warning(
                            "Python Piper created empty file. Switching to CLI."
                        )


            except Exception as e:

                self.logger.warning(
                    f"Python Piper failed: {e}"
                )



            # CLI fallback

            return self._run_cli(
                text,
                file_path
            )


        except Exception as e:

            self.logger.error(
                f"Piper total failure: {e}"
            )

            return self._mock_audio(
                file_path
            )



    def _run_cli(
        self,
        text,
        file_path
    ):

        try:

            self.logger.info(
                "Running Piper CLI..."
            )


            process = subprocess.Popen(
                [
                    "piper",
                    "--model",
                    self.model_path,
                    "--output_file",
                    file_path
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )


            stdout, stderr = process.communicate(
                input=text
            )


            if process.returncode != 0:

                self.logger.error(
                    f"Piper CLI error: {stderr}"
                )

                return self._mock_audio(
                    file_path
                )


            size = os.path.getsize(
                file_path
            )


            if size == 0:

                self.logger.error(
                    "CLI Piper created empty audio"
                )

                return self._mock_audio(
                    file_path
                )


            self.logger.info(
                f"Piper CLI success: {file_path} ({size} bytes)"
            )


            return file_path



        except Exception as e:

            self.logger.error(
                f"Piper CLI failed: {e}"
            )

            return self._mock_audio(
                file_path
            )



    def _mock_audio(
        self,
        file_path
    ):

        import wave
        import struct


        sample_rate = 22050
        duration = 2

        with wave.open(
            file_path,
            "wb"
        ) as wav_file:

            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)


            for _ in range(sample_rate * duration):

                wav_file.writeframes(
                    struct.pack("<h",0)
                )


        self.logger.info(
            f"Mock WAV generated: {file_path}"
        )


        return file_path



piper_service = PiperService()

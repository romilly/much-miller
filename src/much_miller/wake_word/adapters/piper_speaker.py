"""Piper TTS speaker adapter."""

import io
import subprocess
import wave
from pathlib import Path

from piper import PiperVoice

from much_miller.wake_word.ports import SpeakerPort


class PiperSpeaker(SpeakerPort):
    """Speaker adapter using Piper TTS."""

    def __init__(self, model_path: Path) -> None:
        """Initialize the Piper speaker.

        Args:
            model_path: Path to the ONNX voice model file
        """
        self._voice = PiperVoice.load(str(model_path))

    def say(self, text: str) -> None:
        """Speak the given text using Piper TTS.

        Args:
            text: Text to speak
        """
        audio_segments: list[bytes] = []
        for chunk in self._voice.synthesize(text):
            audio_segments.append(chunk.audio_int16_bytes)

        if audio_segments:
            # Add 500ms silence at start to allow audio device to initialize
            silence_samples = int(self._voice.config.sample_rate * 0.5)
            silence = b"\x00\x00" * silence_samples  # 16-bit silence
            audio_data = silence + b"".join(audio_segments)
            wav_bytes = self._to_wav(audio_data)
            subprocess.run(["aplay", "-q", "-"], input=wav_bytes, check=True)

    def _to_wav(self, audio_data: bytes) -> bytes:
        """Convert raw audio bytes to WAV format."""
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self._voice.config.sample_rate)
            wav_file.writeframes(audio_data)
        return wav_buffer.getvalue()

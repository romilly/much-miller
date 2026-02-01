"""Abstract base class for speech-to-text transcription."""

from abc import ABC, abstractmethod


class TranscriberPort(ABC):
    """Abstract base class for speech-to-text transcription services."""

    @abstractmethod
    def transcribe(self, audio_wav: bytes) -> str:
        """Transcribe audio data to text.

        Args:
            audio_wav: WAV-encoded audio bytes

        Returns:
            Transcribed text
        """

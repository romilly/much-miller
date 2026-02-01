"""Abstract base class for voice activity detection."""

from abc import ABC, abstractmethod


class VoiceDetectorPort(ABC):
    """Abstract base class for voice activity detection."""

    @abstractmethod
    def contains_speech(self, audio_wav: bytes) -> bool:
        """Check if audio contains speech.

        Args:
            audio_wav: WAV-encoded audio bytes

        Returns:
            True if speech detected, False otherwise
        """

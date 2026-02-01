"""Abstract base class for audio recording."""

from abc import ABC, abstractmethod


class AudioRecorderPort(ABC):
    """Abstract base class for audio recording services."""

    @abstractmethod
    def record_chunk(self, duration_seconds: float) -> bytes:
        """Record a chunk of audio from the microphone.

        Args:
            duration_seconds: Duration to record

        Returns:
            WAV-encoded audio bytes
        """

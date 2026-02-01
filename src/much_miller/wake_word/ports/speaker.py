"""Abstract base class for text-to-speech output."""

from abc import ABC, abstractmethod


class SpeakerPort(ABC):
    """Abstract base class for text-to-speech services."""

    @abstractmethod
    def say(self, text: str) -> None:
        """Speak the given text.

        Args:
            text: Text to speak
        """

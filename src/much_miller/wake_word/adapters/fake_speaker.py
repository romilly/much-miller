"""Fake speaker for testing."""

from much_miller.wake_word.ports import SpeakerPort


class FakeSpeaker(SpeakerPort):
    """Fake speaker that stores spoken text for test assertions."""

    def __init__(self) -> None:
        self._spoken_text = ""

    @property
    def spoken_text(self) -> str:
        """Return all text that has been spoken."""
        return self._spoken_text

    def say(self, text: str) -> None:
        """Store the spoken text.

        Args:
            text: Text to speak (stored for assertions)
        """
        self._spoken_text += text

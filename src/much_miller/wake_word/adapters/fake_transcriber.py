"""Fake transcriber for testing."""

from much_miller.wake_word.ports import TranscriberPort


class FakeTranscriber(TranscriberPort):
    """Fake transcriber that returns pre-configured responses."""

    def __init__(self, response: str = "") -> None:
        self._response = response

    def set_response(self, response: str) -> None:
        """Set the response to return from transcribe."""
        self._response = response

    def transcribe(self, audio_wav: bytes) -> str:
        """Return the pre-configured response.

        Args:
            audio_wav: WAV-encoded audio bytes (ignored)

        Returns:
            The pre-configured response text
        """
        return self._response

"""Fake voice detector for testing."""

from much_miller.wake_word.ports import VoiceDetectorPort


class FakeVoiceDetector(VoiceDetectorPort):
    """Fake voice detector that returns a configured value."""

    def __init__(self, has_speech: bool = True) -> None:
        self._has_speech = has_speech

    def contains_speech(self, audio_wav: bytes) -> bool:
        """Return the configured value.

        Args:
            audio_wav: WAV-encoded audio bytes (ignored)

        Returns:
            The pre-configured value
        """
        return self._has_speech

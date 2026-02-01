"""Fake audio recorder for testing."""

from much_miller.wake_word.ports import AudioRecorderPort


class FakeRecorder(AudioRecorderPort):
    """Fake audio recorder that returns pre-configured WAV bytes."""

    def __init__(self, wav_bytes: bytes = b"") -> None:
        self._wav_bytes = wav_bytes

    def set_wav_bytes(self, wav_bytes: bytes) -> None:
        """Set the WAV bytes to return from record_chunk."""
        self._wav_bytes = wav_bytes

    def record_chunk(self, duration_seconds: float) -> bytes:
        """Return the pre-configured WAV bytes.

        Args:
            duration_seconds: Duration to record (ignored)

        Returns:
            The pre-configured WAV bytes
        """
        return self._wav_bytes

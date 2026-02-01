"""Port definitions (abstract base classes) for wake word detection."""

from much_miller.wake_word.ports.transcriber import TranscriberPort
from much_miller.wake_word.ports.audio_recorder import AudioRecorderPort

__all__ = ["TranscriberPort", "AudioRecorderPort"]

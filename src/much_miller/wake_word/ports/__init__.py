"""Port definitions (abstract base classes) for wake word detection."""

from much_miller.wake_word.ports.audio_recorder import AudioRecorderPort
from much_miller.wake_word.ports.speaker import SpeakerPort

__all__ = [
    "AudioRecorderPort",
    "SpeakerPort",
]

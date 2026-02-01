"""Adapter implementations for wake word detection."""

from much_miller.wake_word.adapters.http_transcriber import HttpTranscriber
from much_miller.wake_word.adapters.fake_transcriber import FakeTranscriber
from much_miller.wake_word.adapters.sounddevice_recorder import SoundDeviceRecorder
from much_miller.wake_word.adapters.fake_recorder import FakeRecorder

__all__ = [
    "HttpTranscriber",
    "FakeTranscriber",
    "SoundDeviceRecorder",
    "FakeRecorder",
]

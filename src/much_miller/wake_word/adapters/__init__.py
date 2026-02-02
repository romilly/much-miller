"""Adapter implementations for wake word detection."""

from much_miller.wake_word.adapters.sounddevice_recorder import SoundDeviceRecorder
from much_miller.wake_word.adapters.fake_recorder import FakeRecorder
from much_miller.wake_word.adapters.fake_speaker import FakeSpeaker
from much_miller.wake_word.adapters.piper_speaker import PiperSpeaker

__all__ = [
    "SoundDeviceRecorder",
    "FakeRecorder",
    "FakeSpeaker",
    "PiperSpeaker",
]

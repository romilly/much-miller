"""Adapter implementations for wake word detection."""

from much_miller.wake_word.adapters.http_transcriber import HttpTranscriber
from much_miller.wake_word.adapters.fake_transcriber import FakeTranscriber
from much_miller.wake_word.adapters.sounddevice_recorder import SoundDeviceRecorder
from much_miller.wake_word.adapters.fake_recorder import FakeRecorder
from much_miller.wake_word.adapters.fake_speaker import FakeSpeaker
from much_miller.wake_word.adapters.piper_speaker import PiperSpeaker
from much_miller.wake_word.adapters.fake_voice_detector import FakeVoiceDetector
from much_miller.wake_word.adapters.webrtc_voice_detector import WebRtcVoiceDetector

__all__ = [
    "HttpTranscriber",
    "FakeTranscriber",
    "SoundDeviceRecorder",
    "FakeRecorder",
    "FakeSpeaker",
    "PiperSpeaker",
    "FakeVoiceDetector",
    "WebRtcVoiceDetector",
]

"""Tests for voice detector adapters."""

import io
import wave

import numpy as np
from hamcrest import assert_that, is_

from much_miller.wake_word.adapters import FakeVoiceDetector, WebRtcVoiceDetector


class TestFakeVoiceDetector:
    """Tests for FakeVoiceDetector adapter."""

    def test_returns_configured_value(self) -> None:
        detector = FakeVoiceDetector(has_speech=True)

        result = detector.contains_speech(b"fake audio")

        assert_that(result, is_(True))

    def test_returns_false_when_configured(self) -> None:
        detector = FakeVoiceDetector(has_speech=False)

        result = detector.contains_speech(b"fake audio")

        assert_that(result, is_(False))


def create_silent_wav(duration_seconds: float = 0.5, sample_rate: int = 16000) -> bytes:
    """Create a WAV file with silence."""
    num_samples = int(sample_rate * duration_seconds)
    samples = np.zeros(num_samples, dtype=np.int16)
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(samples.tobytes())
    return buffer.getvalue()


def create_noisy_wav(duration_seconds: float = 0.5, sample_rate: int = 16000) -> bytes:
    """Create a WAV file with noise (simulating speech)."""
    num_samples = int(sample_rate * duration_seconds)
    # Generate random noise with significant amplitude
    samples = np.random.randint(-20000, 20000, num_samples, dtype=np.int16)
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(samples.tobytes())
    return buffer.getvalue()


class TestWebRtcVoiceDetector:
    """Tests for WebRtcVoiceDetector adapter."""

    def test_returns_false_for_silence(self) -> None:
        detector = WebRtcVoiceDetector()
        silent_audio = create_silent_wav()

        result = detector.contains_speech(silent_audio)

        assert_that(result, is_(False))

    def test_returns_true_for_noise(self) -> None:
        detector = WebRtcVoiceDetector()
        noisy_audio = create_noisy_wav()

        result = detector.contains_speech(noisy_audio)

        assert_that(result, is_(True))

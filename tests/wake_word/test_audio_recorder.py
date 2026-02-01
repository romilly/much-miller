"""Integration tests for SoundDeviceRecorder."""

import wave
import io

import pytest
from hamcrest import assert_that, greater_than, is_

from much_miller.wake_word.adapters import SoundDeviceRecorder


def microphone_available() -> bool:
    """Check if a microphone is available."""
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        return any(d['max_input_channels'] > 0 for d in devices)
    except Exception:
        return False


requires_microphone = pytest.mark.skipif(
    not microphone_available(),
    reason="No microphone available"
)


class TestSoundDeviceRecorder:
    """Integration tests for SoundDeviceRecorder."""

    @requires_microphone
    def test_record_chunk_returns_valid_wav_bytes(self) -> None:
        recorder = SoundDeviceRecorder()

        wav_bytes = recorder.record_chunk(duration_seconds=0.5)

        # Verify it's valid WAV data
        buffer = io.BytesIO(wav_bytes)
        with wave.open(buffer, 'rb') as wav_file:
            assert_that(wav_file.getnchannels(), is_(1))
            assert_that(wav_file.getsampwidth(), is_(2))
            assert_that(wav_file.getframerate(), is_(16000))
            assert_that(wav_file.getnframes(), greater_than(0))
